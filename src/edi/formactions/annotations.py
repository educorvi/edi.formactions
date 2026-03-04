from persistent.list import PersistentList
from plone import api
from zope.annotation.interfaces import IAnnotations

# imports from edi.formactions
from edi.formactions.config import ANNOTATION_KEY


class AnnotationData(object):
    """Helper class to structure annotation data for form actions"""

    user_id: str
    json_data: dict
    # json_schema: dict
    # ui_schema: dict

    def __init__(
        self,
        user_id: str,
        json_data: dict,
        # json_schema: dict = None,
        # ui_schema: dict = None,
    ):
        self.user_id = user_id
        self.json_data = json_data
        # self.json_schema = json_schema
        # self.ui_schema = ui_schema

    def to_dict(self) -> dict:
        """Convert the annotation data to a dictionary format"""
        return {
            "user_id": self.user_id,
            "json_data": self.json_data,
            # "json_schema": self.json_schema,
            # "ui_schema": self.ui_schema,
        }


class FormActionsAnnotationStorage(object):
    """Helper class to manage form action data stored in annotations"""

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        if ANNOTATION_KEY not in annotations.keys():
            annotations[ANNOTATION_KEY] = PersistentList()
        self.annotations = annotations[ANNOTATION_KEY]

    def store_as_annotation(self, json_data: dict):
        """Add a new entry to the annotation storage of the context"""
        user = api.user.get_current()
        user_id = user.getUserId() if user else "anonymous"
        annotation_data = AnnotationData(
            user_id=user_id,
            json_data=json_data,
            # json_schema=json_schema,
            # ui_schema=ui_schema
        )
        self.annotations.append(annotation_data.to_dict())

    def get_all_annotations(self) -> list:
        """Retrieve all annotations from the storage"""
        return self.annotations
