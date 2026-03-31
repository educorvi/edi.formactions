# from plone.app.textfield import RichText
# from plone.autoform import directives
from edi.formactions.content.generic_handler import GenericHandler
from edi.formactions.content.generic_handler import IGenericHandler

# from plone.namedfile import field as namedfile
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope.interface import implementer


class IAnnotationStorageHandler(IGenericHandler):
    """Marker interface and Dexterity Python Schema for AnnotationStorageHandler"""


@implementer(IAnnotationStorageHandler)
class AnnotationStorageHandler(GenericHandler):
    """Content-type class for IAnnotationStorageHandler"""
