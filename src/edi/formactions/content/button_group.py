from edi.formactions import _
from edi.jsonforms.content.common import IFormElement
from plone.dexterity.content import Container
from zope.interface import implementer


class IButtonGroup(IFormElement):
    """Marker interface and Dexterity Python Schema for ButtonGroup"""


@implementer(IButtonGroup)
class ButtonGroup(Container):
    """Content-type class for IButtonGroup"""
