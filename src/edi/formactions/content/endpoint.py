# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Container

# from plone.namedfile import field as namedfile
from plone.supermodel import model

# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer


from edi.formactions import _


class IEndpoint(model.Schema):
    """Marker interface and Dexterity Python Schema for Endpoint"""

    url = schema.URI(
        title=_("Endpoint URL"),
        description=_("The URL of the endpoint to which requests will be sent."),
        required=True,
    )

    api_key_header_name = schema.TextLine(
        title=_("Header Name for API Key"),
        description=_("The name of the header where the API key will be sent."),
        required=False,
    )

    api_key = schema.TextLine(
        title=_("API Key"),
        description=_("The API key to be used for this endpoint."),
        required=False,
    )


@implementer(IEndpoint)
class Endpoint(Container):
    """Content-type class for IEndpoint"""
