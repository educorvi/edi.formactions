# -*- coding: utf-8 -*-

# from edi.formactions import _
import json

from plone import api
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IJsonFormsDocumentView(Interface):
    """Marker Interface for IJsonFormsDocumentView"""


@implementer(IJsonFormsDocumentView)
class JsonFormsDocumentView(BrowserView):
    def __call__(self):
        return self.index()

    def get_ui_schema(self):
        disable_save_button = False
        user = api.user.get_current()
        if not user:
            disable_save_button = True
        if self.context.Creator() != user.getUserId() and not api.user.has_permission(
            "Modify portal content", obj=self.context
        ):
            disable_save_button = True

        ui_schema = json.loads(self.context.ui_schema) if self.context.ui_schema else {}
        if "layout" in ui_schema.keys():
            layout = ui_schema["layout"]
            if "elements" in layout.keys():
                buttongroup = layout["elements"][-1]
                if (
                    buttongroup["type"] == "Buttongroup"
                    and "buttons" in buttongroup.keys()
                ):
                    button = buttongroup["buttons"][0]
                    if "options" in button.keys():
                        ui_schema["layout"]["elements"][-1]["buttons"][0]["options"][
                            "disabled"
                        ] = disable_save_button  # disable the save button if the user is not allowed to edit the content
        return json.dumps(
            ui_schema,
            ensure_ascii=False,
            indent=4,
        )
