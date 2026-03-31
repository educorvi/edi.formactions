# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from edi.formactions import _
from plone.dexterity.content import Container

# from plone.namedfile import field as namedfile
from plone.supermodel import model

# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer


class IJsonFormsDocument(model.Schema):
    """Marker interface and Dexterity Python Schema for JsonFormsDocument"""

    json_data = schema.Text(
        title=_("Json data"),
        description=_("This field stores the json data of the filled form."),
        required=True,
    )

    json_schema = schema.Text(
        title=_("Json schema"),
        description=_("This field stores the json schema of the form."),
        required=True,
    )

    ui_schema = schema.Text(
        title=_("UI schema"),
        description=_("This field stores the ui schema of the form."),
        required=True,
    )


@implementer(IJsonFormsDocument)
class JsonFormsDocument(Container):
    """Content-type class for IJsonFormsDocument"""
