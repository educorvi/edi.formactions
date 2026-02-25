# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import alsoProvides
from zExceptions import BadRequest
from zope.component import getUtility
from Products.MailHost.interfaces import IMailHost
from plone.api import portal
from plone.base.utils import getToolByName, safe_text
from plone.protect.interfaces import IDisableCSRFProtection
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from edi.formactions import _
from edi.formactions.annotations import FormActionsAnnotationStorage
from jinja2 import Template, meta
from jinja2.sandbox import SandboxedEnvironment

from edi.jsonforms.views.json_schema_view import JsonSchemaView
from edi.jsonforms.views.ui_schema_view import UiSchemaView


def load_form_action_data(handler_post: Service) -> dict:
    """Helper function to load form action data from the request"""
    data = handler_post.request.get("BODY", None)
    if not data:
        raise BadRequest("No data provided.")

    if isinstance(data, bytes):
        data = data.decode("utf-8")

    return data


class FormActionsEmailHandlerPost(Service):
    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        default_sender = api.portal.get_registry_record(
            "plone.email_from_address", default="noreply@plone.org"
        )
        data = load_form_action_data(self)

        # try:
        #     payload = json.loads(data)
        # except json.JSONDecodeError:
        #     raise BadRequest("Invalid JSON format.")
        recipient = self.request.form.get("to_address")
        reply_to = self.request.form.get("reply_to_address", None)
        subject = self.request.form.get("subject", _("No Subject"))
        message = self.request.form.get("email_text", "") + "\n"

        message += data

        if not recipient:
            raise BadRequest("Recipient email address is required.")

        # Send email
        response = self.send_email(
            recipient, default_sender, reply_to, subject, message
        )

        self.request.response.setStatus(200)
        return response

    def send_email(self, recipient, sender, reply_to_adress, subject, message):
        """Helper method to send email."""

        messageText = MIMEMultipart()
        messageText.attach(MIMEText(message, "plain", "utf-8"))
        messageText["Subject"] = subject
        if reply_to_adress:
            messageText["Reply-To"] = reply_to_adress

        # Send the email
        try:
            api.portal.send_email(
                recipient=recipient,
                sender=sender,
                subject=subject,
                body=messageText,
            )
            return

        except Exception as e:
            raise BadRequest(f"Failed to send email: {str(e)}")


class FormActionsWebserviceHandlerPost(Service):
    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        data = load_form_action_data(self)

        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            raise BadRequest("Invalid JSON format.")

        endpoints = []
        i = 1
        while True:
            if f"endpoint_{i}_url" not in self.request.form:
                break
            url = self.request.form.get(f"endpoint_{i}_url")
            endpoint = {
                "url": url,
            }
            api_key_header_name = self.request.form.get(
                f"endpoint_{i}_api_key_header_name", None
            )
            api_key = self.request.form.get(f"endpoint_{i}_api_key", None)
            if api_key_header_name and api_key:
                endpoint[api_key_header_name] = api_key
            endpoints.append(endpoint)
            i += 1

        page_after_success = self.request.form.get("page_after_success", None)

        self.request.response.setStatus(200)
        status = "success"
        message = _("Web service request sent successfully.")
        error_message = _("Error sending request to: ")
        error_occurred = False
        for endpoint in endpoints:
            headers = {k: v for k, v in endpoint.items() if k != "url"}
            headers["Referer"] = "https://plone.org"  # self.context.absolute_url()
            response = requests.post(
                url=endpoint["url"], headers=headers, data=json.dumps(payload)
            )

            if response.status_code != 200:
                error_occurred = True
                self.request.response.setStatus(400)
                status = "error"
                error_message += f"{endpoint['url']}: {response.text}, "

        if error_occurred:
            api.portal.show_message(
                message=error_message, request=self.request, type="error"
            )
        elif page_after_success:
            self.request.response.redirect(page_after_success)
        else:
            return {"status": status, "message": message}


class FormActionsStorageHandlerPost(Service):
    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        data = load_form_action_data(self)

        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            raise BadRequest("Invalid JSON format.")

        annotation_storage = FormActionsAnnotationStorage(self.context)
        annotation_storage.store_as_annotation(payload)

        page_after_success = self.request.form.get("page_after_success", None)

        self.request.response.setStatus(200)
        if page_after_success:
            self.request.response.redirect(page_after_success)
        else:
            return {"status": "success", "message": _("Data stored successfully.")}


class FormActionsFileStorageHandlerPost(Service):
    """Handler for storing form data in a file inside a folder in the Plone site."""

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        data = load_form_action_data(self)

        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            raise BadRequest("Invalid JSON format.")

        # get target folder from request form and validate it
        folder_path = self.request.form.get("folder_path")
        if not folder_path:
            raise BadRequest("File path is required.")
        folder = api.content.get(path=folder_path)
        if folder is None:
            raise BadRequest("Folder path is invalid.")

        # get content object title from request form, validate it and render it as jinja2 template with form data as variables
        content_object_title = self.request.form.get(
            "content_object_title", _("Form submission")
        )
        env = SandboxedEnvironment()
        obj_title = env.from_string(content_object_title).render(
            data=payload, user=api.user.get_current()
        )

        # ast = env.parse(content_object_title)
        # variables = meta.find_undeclared_variables(ast)
        # obj_title = Template(content_object_title)
        # render_vars = {"data": payload, "user": api.user.get_current()}
        # obj_title = obj_title.render(**render_vars)
        if not obj_title or obj_title.isspace():
            obj_title = _("Form submission")
        obj_id = safe_text(obj_title.lower().replace(" ", "-"))

        # create JsonFormsDocument inside the target folder but bypass permission checks
        # necessary because not logged in users can also submit forms
        portal_types = getToolByName(portal, "portal_types")
        type_info = portal_types.getTypeInfo("JsonFormsDocument")
        # test if object with id already exists in folder, append a number if necessary
        obj_path = f"{folder_path}/{obj_id}"
        if api.content.get(path=obj_path):
            i = 1
            while True:
                obj_id = f"{obj_id}-{i}"
                if not api.content.get(path=f"{folder_path}/{obj_id}"):
                    break
                i += 1
        jsonformsdocument = type_info._constructInstance(
            folder, obj_id, title=obj_title
        )

        # set fields of the created object
        jsonformsdocument.json_data = json.dumps(payload, ensure_ascii=False, indent=4)
        jsonformsdocument.json_schema = JsonSchemaView(self.context, self.request)()
        ui_schema = json.loads(UiSchemaView(self.context, self.request)())
        # remove all buttongroups
        for i, element in enumerate(ui_schema.get("layout", []).get("elements", [])):
            if element.get("type") == "Buttongroup":
                ui_schema["layout"]["elements"].pop(i)
        # put new buttongroup into the ui schema to enable editing the created JsonFormsDocument
        new_button_group = {
            "type": "Buttongroup",
            "buttons": [
                {
                    "type": "Button",
                    "buttonType": "submit",
                    "text": _("Save"),
                    "options": {
                        "variant": "secondary",
                        "submitOptions": {
                            "action": "request",
                            "request": {
                                "url": f"{jsonformsdocument.absolute_url()}/@edit-jsonformsdocument",
                                "method": "POST",
                                "headers": {
                                    "Accept": "application/json",
                                    "Content-Type": "application/json",
                                },
                            },
                        },
                    },
                }
            ],
        }
        ui_schema["layout"]["elements"].append(new_button_group)
        jsonformsdocument.ui_schema = json.dumps(
            ui_schema, ensure_ascii=False, indent=4
        )

        page_after_success = self.request.form.get("page_after_success", None)

        self.request.response.setStatus(200)
        if page_after_success:
            self.request.response.redirect(page_after_success)
        else:
            return {
                "status": "success",
                "message": _("Data stored in folder successfully."),
                "edi.jsonforms": {
                    "redirect_to": jsonformsdocument.absolute_url(),
                },
            }


class FormActionsEditJsonFormsDocumentPost(Service):
    """Endpoint to edit a JsonFormsDocument created by the FormActionsFileStorageHandler"""

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        data = load_form_action_data(self)

        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            raise BadRequest("Invalid JSON format.")

        # update json_data field of the context JsonFormsDocument with the new data
        self.context.json_data = json.dumps(payload, ensure_ascii=False, indent=4)

        self.request.response.setStatus(200)
        return {"status": "success", "message": _("Data updated successfully.")}
