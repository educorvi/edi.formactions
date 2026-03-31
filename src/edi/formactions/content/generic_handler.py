from edi.formactions import _
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IGenericHandler(model.Schema):
    """Marker interface and Dexterity Python Schema for GenericHandler"""


@implementer(IGenericHandler)
class GenericHandler(Container):
    """Content-type class for IGenericHandler"""
