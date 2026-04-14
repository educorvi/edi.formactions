import csv
import io
import json

from edi.formactions.views.annotations_view import AnnotationsView
from zope.interface import implementer
from zope.interface import Interface
from Products.Five.browser import BrowserView

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IPotenzialanalyseView(Interface):
    """Marker Interface for IPotenzialanalyseView"""


class PotenzialanalyseHelper:
    MAPPING = {
        "not": "Nicht relevant",
        "ready": "Bereits angeboten",
        "standard": "Soll der Standardweg sein",
        "important": "Wichtig für die Realisierung",
        "condition": "Notwendige Bedingung für die Realisierung",
    }

    COLUMNS = [
        ("service_id", "Service ID"),
        ("service_title", "Service Titel"),
        ("service_description", "Service Beschreibung"),
        ("mandant", "Mandant"),
        ("bearbeitung_durch", "Bearbeitung durch"),
        ("fachbereich", "Fachbereich"),
        ("status", "Status"),
        ("fachdomaene", "Fachdomäne"),
        ("fachbereich_subdomaene", "MuB Fachbereich / Subdomäne RuL/Prävention"),
        ("querschnittsthemen", "Querschnittsthemen"),
        ("list_potenziale", "Potenziale"),
        ("potenziale_weitere", "Weitere Potenziale"),
        ("browser", "Browser"),
        ("app_pwa", "App/PWA"),
        ("api", "API"),
        ("chatbot", "Chatbot"),
        ("ki_assistenz", "KI-Assistent"),
        ("automatisierung", "Automatisierung"),
        ("aufwand", "Aufwand"),
        ("ideen", "Ideen"),
    ]

    def __call__(self):
        if self.request.form.get("download") == "csv":
            csv_content = self._build_csv(self.get_services())
            self.request.response.setHeader("Content-Type", "text/csv; charset=utf-8")
            self.request.response.setHeader(
                "Content-Disposition", 'attachment; filename="potenzialanalyse.csv"'
            )
            return "\ufeff" + csv_content
        return self.index()

    def _as_csv_cell(self, value):
        if isinstance(value, list):
            return " | ".join(str(v) for v in value)
        return value if value is not None else ""

    def _build_csv(self, services):
        output = io.StringIO()
        writer = csv.writer(output, delimiter=";")
        writer.writerow([header for _, header in self.COLUMNS])
        for service in services:
            writer.writerow(
                [self._as_csv_cell(service.get(field, "")) for field, _ in self.COLUMNS]
            )
        return output.getvalue()

    def create_service(self, json_data: dict) -> dict:
        with open(
            "src/edi.formactions/src/edi/formactions/views/mapping_service_ids.json",
            "r",
            encoding="utf-8",
        ) as f:
            service = {}

            service_id_mapping = json.load(f)
            service_id = json_data.get("service_id", "")
            service["service_id"] = service_id

            service_title_original = service_id_mapping.get(str(service_id), {}).get(
                "name", ""
            )
            service_title = json_data.get("service_title", "") or json_data.get(
                "service_title_new", ""
            )
            service["service_title"] = (
                f"{service_title} ({service_title_original})"
                if service_title_original
                else service_title
            )

            info = {
                "service_description": json_data.get("service_description_new", ""),
                "mandant": json_data.get("mandant", ""),
                "bearbeitung_durch": json_data.get("bearbeitung_durch", ""),
                "fachbereich": json_data.get("fachbereich", ""),
                "status": json_data.get("status", ""),
                "fachdomaene": json_data.get("fachdomaene", ""),
                "fachbereich_subdomaene": json_data.get("mub_fachbereich", "")
                or json_data.get("subdomaenen_rul", "")
                or json_data.get("subdomaenen_praev", ""),
                "querschnittsthemen": json_data.get("querschnittsthemen", ""),
                "list_potenziale": json_data.get("list_potenziale", ""),
                "potenziale_weitere": json_data.get("potenziale_weitere", ""),
                "browser": self.MAPPING.get(json_data.get("browser", ""), ""),
                "app_pwa": self.MAPPING.get(json_data.get("app_pwa", ""), ""),
                "api": self.MAPPING.get(json_data.get("api", ""), ""),
                "chatbot": json_data.get("chatbot", ""),
                "ki_assistenz": json_data.get("ki_assistenz", ""),
                "automatisierung": json_data.get("automatisierung", ""),
                "aufwand": json_data.get("aufwand", ""),
                "ideen": json_data.get("ideen", ""),
            }

            service.update(info)
            return service


@implementer(IPotenzialanalyseView)
class AnnotationsPotenzialanalyseView(PotenzialanalyseHelper, AnnotationsView):
    """
    View for a form (IForm) that contains annotations with the form data of the filled form (created by the formaction annotation_storage_handler)
    """

    def get_services(self):
        annotations = self.get_annotations()
        services = []
        for annotation in annotations:
            json_data = annotation["json_data"]
            service = self.create_service(json_data)
            services.append(service)
        return services


@implementer(IPotenzialanalyseView)
class JFDPotenzialanalyseView(PotenzialanalyseHelper, BrowserView):
    """
    View for a folder that contains JsonFormsDocuments (created by the formaction file_storage_handler)
    """

    def get_services(self):
        jfds = self.context.restrictedTraverse("contentlisting")()
        services = []
        for jfd in jfds:
            if jfd.portal_type != "JsonFormsDocument":
                continue
            json_data_str = getattr(jfd, "json_data", "{}")
            json_data = json.loads(json_data_str)
            service = self.create_service(json_data)
            services.append(service)
        return services
