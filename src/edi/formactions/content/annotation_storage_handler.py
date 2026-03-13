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
from edi.formactions.content.generic_handler import IGenericHandler, GenericHandler


class IAnnotationStorageHandler(IGenericHandler):
    """Marker interface and Dexterity Python Schema for AnnotationStorageHandler"""


@implementer(IAnnotationStorageHandler)
class AnnotationStorageHandler(GenericHandler):
    """Content-type class for IAnnotationStorageHandler"""
