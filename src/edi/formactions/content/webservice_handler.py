# -*- coding: utf-8 -*-
from zope import schema
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


from edi.formactions import _
from edi.formactions.content.generic_handler import IGenericHandler, GenericHandler


class IWebserviceHandler(IGenericHandler):
    """ Marker interface and Dexterity Python Schema for WebserviceHandler
    """


@implementer(IWebserviceHandler)
class WebserviceHandler(GenericHandler):
    """ Content-type class for IWebserviceHandler
    """
