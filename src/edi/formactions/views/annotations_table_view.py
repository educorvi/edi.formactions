import csv
import io
import json
from typing import Any

from edi.formactions.views.annotations_view import AnnotationsView
from edi.jsonforms.views.json_schema_view import JsonSchemaView
from zope.interface import implementer
from zope.interface import Interface
from Products.Five.browser import BrowserView


class IAnnotationsTableView(Interface):
    """Marker Interface for IAnnotationsTableView"""


class AnnotationsTableHelper:
    def flatten_dict(
        self, data: dict[str, Any], parent_key: str = ""
    ) -> dict[str, Any]:
        """
        Flatten nested dict keys using dot notation.

        Example:
            {"a": "hallo", "b": {"a": "hallo"}} -> {"a": "hallo", "b.a": "hallo"}
        """
        flattened: dict[str, Any] = {}

        for key, value in data.items():
            new_key = f"{parent_key}.{key}" if parent_key else str(key)

            if isinstance(value, dict):
                flattened.update(self.flatten_dict(value, new_key))
            else:
                flattened[new_key] = value

        return flattened

    def process_uploads(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Process the uploads in the data and replace the file data with the filename.

        Example:
            {"file": "data:application/pdf;name=example.pdf;base64,..." } -> {"file": "example.pdf"}
        """
        for key, value in data.items():
            if isinstance(value, str) and ";base64," in value and ";name=" in value:
                filename = value.split(";name=")[1].split(";")[0]
                data[key] = filename
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    if (
                        isinstance(item, str)
                        and ";base64," in item
                        and ";name=" in item
                    ):
                        filename = item.split(";name=")[1].split(";")[0]
                        value[index] = filename
        return data

    def get_processed_keys(self, data: dict[str, Any]) -> list[str]:
        """
        Flatten the dict and remove keys of objects and array elements

        Return list of keys
        """
        flattened_dict = self.flatten_dict(data)

        flattened_list = [
            key.replace("properties.", "").replace("items.", "").replace(".title", "")
            for key in flattened_dict
            if key.endswith(".title") and ".items.properties." not in key
        ]

        # remove keys of arrays and objects
        del_keys = []
        for key in flattened_list:
            if len([k for k in flattened_list if k.startswith(key)]) > 1:
                del_keys.append(key)

        for key in del_keys:
            flattened_list.remove(key)

        return flattened_list

    def __call__(self):
        if self.request.form.get("download") == "tsv":
            tsv_content = self._build_tsv(self.create_table_data())
            self.request.response.setHeader(
                "Content-Type", "text/tab-separated-values; charset=utf-8"
            )
            self.request.response.setHeader(
                "Content-Disposition", 'attachment; filename="annotations.tsv"'
            )
            return "\ufeff" + tsv_content
        return self.index()

    def _as_tsv_cell(self, value):
        if isinstance(value, list):
            return " | ".join(str(v) for v in value)
        return value if value is not None else ""

    def _build_tsv(self, table_data: dict[str, Any], columns: list[str]) -> str:
        output = io.StringIO()
        writer = csv.writer(output, delimiter="\t")
        writer.writerow([header for _, header in columns])
        for service in table_data:
            writer.writerow(
                [self._as_tsv_cell(service.get(field, "")) for field in columns]
            )
        return output.getvalue()

    def create_table_data(self, json_data: dict) -> dict:
        table_data = self.flatten_dict(json_data)
        table_data = self.process_uploads(table_data)
        return table_data


@implementer(IAnnotationsTableView)
class AnnotationsTableView(AnnotationsTableHelper, AnnotationsView):
    """
    View for a form (IForm) that contains annotations with the form data of the filled form (created by the formaction annotation_storage_handler)
    """

    columns: list

    def __init__(self, context, request):
        super().__init__(context, request)
        self.columns = []

    def get_rows(self):
        annotations = self.get_annotations()
        table_rows = []
        for annotation in annotations:
            table_row = self.create_table_data(annotation["json_data"])
            table_rows.append(table_row)

        return table_rows

    def get_columns(self):
        """
        Get the columns for the table by flattening the JSON schema of the form and using the keys as column names.
        Necessary because the json_data does not contain the order of the fields and the table should be displayed in the order of the JSON schema.
        """
        json_schema_view = JsonSchemaView(self.context, self.request)
        json_schema = json_schema_view.get_schema()
        self.columns = self.get_processed_keys(json_schema)
        return self.columns


# @implementer(IAnnotationsTableView)
# class JFDPotenzialanalyseView(AnnotationsTableHelper, BrowserView):
#     """
#     View for a folder that contains JsonFormsDocuments (created by the formaction file_storage_handler)
#     """

#     def get_services(self):
#         jfds = self.context.restrictedTraverse("contentlisting")()
#         services = []
#         for jfd in jfds:
#             if jfd.portal_type != "JsonFormsDocument":
#                 continue
#             json_data_str = getattr(jfd, "json_data", "{}")
#             json_data = json.loads(json_data_str)
#             service = self.create_table_data(json_data)
#             service["link"] = jfd.getURL()
#             services.append(service)

#         return services
