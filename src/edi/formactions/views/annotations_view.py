# from edi.formactions import _
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from edi.formactions.annotations import FormActionsAnnotationStorage
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface


class IAnnotationsView(Interface):
    """Marker Interface for IAnnotationsView"""


@implementer(IAnnotationsView)
class AnnotationsView(BrowserView):
    def __call__(self):
        return self.index()

    def get_annotations(self):
        """Method to get annotations of the context"""
        annotation_storage = FormActionsAnnotationStorage(self.context)
        return annotation_storage.get_all_annotations()
