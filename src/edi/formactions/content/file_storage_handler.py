# -*- coding: utf-8 -*-
from plone.app.z3cform.widget import RelatedItemsFieldWidget

# from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container

# from plone.namedfile import field as namedfile
from plone.supermodel import model

# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


from edi.formactions import _
from edi.formactions.content.generic_handler import IGenericHandler
from edi.formactions.content.generic_handler import GenericHandler


class IFileStorageHandler(IGenericHandler):
    """Marker interface and Dexterity Python Schema for FileStorageHandler"""

    file_path = RelationChoice(
        title=_("Target folder for file storage"),
        description=_(
            "Select the folder where the json data of the filled form will be stored."
        ),
        vocabulary="plone.app.vocabularies.Catalog",
        required=True,
    )

    content_object_title = schema.TextLine(
        title=_("Title for stored content objects"),
        description=_(
            "Define a title for the content objects that will be created to store the json data of the filled form. Use the jinja2 language to define dynamic titles. E.g. 'Form submission from {{id_of_field_x}} on {{id_of_field_y}}'."
        ),
        required=False,
    )

    directives.widget(
        "file_path",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["Folder"]},
    )


@implementer(IFileStorageHandler)
class FileStorageHandler(GenericHandler):
    """Content-type class for IFileStorageHandler"""
