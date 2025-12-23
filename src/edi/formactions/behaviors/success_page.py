from edi.jsonforms.content.form import IForm
from zope.interface import provider
from edi.formactions import _
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from plone.autoform.interfaces import IFormFieldProvider

from plone.app.textfield import RichText
from zope.interface.declarations import implementer
from zope.interface import Interface

from plone.base.utils import safe_hasattr

class ISuccessPageMarker(Interface):
    pass

@provider(IFormFieldProvider)
class ISuccessPage(model.Schema):

    fieldset(
        "success_page",
        label=_("Success Page"),
        fields=[
            "success_page"
        ],
    )
    success_page = RichText(
        title=_("Success Page"),
        required=False
    )

@implementer(ISuccessPage)
class SuccessPage(object):
    def __init__(self, context):
        self.context = context

    @property
    def success_page(self):
        if safe_hasattr(self.context, "success_page"):
            return self.context.success_page
        return None

    @success_page.setter
    def success_page(self, value):
        self.context.success_page = value
