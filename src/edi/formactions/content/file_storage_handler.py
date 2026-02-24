# -*- coding: utf-8 -*-
from jinja2 import Environment, TemplateSyntaxError
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer, Invalid, invariant

from edi.formactions import _
from edi.formactions.content.generic_handler import IGenericHandler
from edi.formactions.content.generic_handler import GenericHandler


class IFileStorageHandler(IGenericHandler):
    """Marker interface and Dexterity Python Schema for FileStorageHandler"""

    target_folder = RelationChoice(
        title=_("Target folder for file storage"),
        description=_(
            "Select the folder where the json data of the filled form will be stored. If the folder is deleted, the button will be disabled."
        ),
        vocabulary="plone.app.vocabularies.Catalog",
        required=True,
    )

    content_object_title = schema.TextLine(
        title=_("Title for stored content objects"),
        description=_(
            "Define a title for the content objects that will be created to store the json data of the filled form. Use the jinja2 language to define dynamic titles. E.g. 'Form submission from {{id_of_field_x}} on {{id_of_field_y}}'. The id of the fields must be from fields of the form (the fields cannot be inside an array or object, but can be inside a fieldset). If ids are invalid, the button will be disabled."
        ),
        required=False,
    )

    directives.widget(
        "target_folder",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["Folder"]},
    )

    @invariant
    def validate_content_object_title(data):
        """Validate that the content_object_title field contains valid jinja2 syntax."""
        if data.content_object_title:
            try:
                Environment().from_string(data.content_object_title)
            except TemplateSyntaxError as e:
                raise Invalid(
                    _(
                        f"Invalid jinja2 syntax: {str(e)}",
                    )
                )


@implementer(IFileStorageHandler)
class FileStorageHandler(GenericHandler):
    """Content-type class for IFileStorageHandler"""
