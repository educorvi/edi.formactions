# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Container

# from plone.namedfile import field as namedfile
from plone.supermodel import model

# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


from edi.formactions import _


class IFileStorageHandler(model.Schema):
    """Marker interface and Dexterity Python Schema for FileStorageHandler"""

    dependencies = RelationChoice(
        title=_("Target folder for file storage"),
        description=_(
            "Select the folder where the json data of the filled form will be stored."
        ),
        vocabulary="plone.app.vocabularies.Catalog",
        required=False,
    )

    content_object_title = schema.TextLine(
        title=_("Title for stored content objects"),
        description=_(
            "Define a title for the content objects that will be created to store the json data of the filled form. Use the jinja2 language to define dynamic titles. E.g. 'Form submission from {{id_of_field_x}} on {{id_of_field_y}}'."
        ),
        required=False,
    )


@implementer(IFileStorageHandler)
class FileStorageHandler(Container):
    """Content-type class for IFileStorageHandler"""
