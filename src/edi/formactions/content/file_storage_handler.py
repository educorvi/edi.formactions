# -*- coding: utf-8 -*-
from jinja2 import TemplateSyntaxError
from jinja2.sandbox import SandboxedEnvironment
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
            "Select the folder where the json data of the filled form will be stored. If the folder is deleted, the button will be disabled. The folder must be published if it is possible that users that are not logged in will fill the form, otherwise the content object cannot be created and the form submission will fail."
        ),
        vocabulary="plone.app.vocabularies.Catalog",
        required=True,
    )

    content_object_title = schema.TextLine(
        title=_("Title for stored content objects"),
        description=_(
            "Define a title for the content objects that will be created to store the JSON data of the filled form. Use the Jinja2 language to define dynamic titles. For example: 'Form submission from {{data['id_of_field_x']}} on {{data['id_of_field_y']}}', to use the value of field x and y in the title. This also works if the field is inside a fieldset. The field IDs must come from the form fields. In addition to field values, you can use the username via '{{user}}'."
        ),
        required=False,
    )

    # redirect_to_new_object = schema.Bool(
    #     title=_("Redirect to created content object after submission"),
    #     description=_(
    #         "If enabled, the user will be redirected to the created content object after form submission and the configuration of the page after success is ignored."
    #     ),
    #     required=False,
    #     default=True,
    # )

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
                SandboxedEnvironment().from_string(data.content_object_title)
            except TemplateSyntaxError as e:
                error_message = _(
                    "Invalid jinja2 syntax: ${error}",
                    mapping={"error": str(e)},
                )
                raise Invalid(error_message)


@implementer(IFileStorageHandler)
class FileStorageHandler(GenericHandler):
    """Content-type class for IFileStorageHandler"""
