# -*- coding: utf-8 -*-

# from edi.formactions import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IJsonFormsDocumentView(Interface):
    """ Marker Interface for IJsonFormsDocumentView"""


@implementer(IJsonFormsDocumentView)
class JsonFormsDocumentView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('json_forms_document_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
