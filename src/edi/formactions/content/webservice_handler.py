from edi.formactions.content.generic_handler import GenericHandler
from edi.formactions.content.generic_handler import IGenericHandler
from zope.interface import implementer


class IWebserviceHandler(IGenericHandler):
    """Marker interface and Dexterity Python Schema for WebserviceHandler"""


@implementer(IWebserviceHandler)
class WebserviceHandler(GenericHandler):
    """Content-type class for IWebserviceHandler"""
