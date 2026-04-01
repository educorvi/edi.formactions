# from edi.formactions import _
from plone import api
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface

import json


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
        if not user or (
            self.context.Creator() != user.getUserId()
            and not api.user.has_permission("Modify portal content", obj=self.context)
        ):
            disable_save_button = True

        ui_schema = json.loads(self.context.ui_schema) if self.context.ui_schema else {}
        if "layout" in ui_schema:
            layout = ui_schema["layout"]
            if "elements" in layout:
                buttongroup = layout["elements"][-1]
                if buttongroup["type"] == "Buttongroup" and "buttons" in buttongroup:
                    button = buttongroup["buttons"][0]
                    if "options" in button:
                        ui_schema["layout"]["elements"][-1]["buttons"][0]["options"][
                            "disabled"
                        ] = disable_save_button  # disable the save button if the user
                        # is not allowed to edit the content
        return json.dumps(
            ui_schema,
            ensure_ascii=False,
            indent=4,
        )
