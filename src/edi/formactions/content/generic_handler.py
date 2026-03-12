from plone.supermodel import model
from plone.dexterity.content import Container
from zope import schema
from zope import schema
from zope.interface import implementer
from edi.formactions import _


class IGenericHandler(model.Schema):
    """Marker interface and Dexterity Python Schema for GenericHandler"""


@implementer(IGenericHandler)
class GenericHandler(Container):
    """Content-type class for IGenericHandler"""
