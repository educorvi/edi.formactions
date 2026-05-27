from edi.formactions import _
from edi.formactions.annotations import FormActionsAnnotationStorage
from edi.jsonforms.views.json_schema_view import JsonSchemaView
from edi.jsonforms.views.ui_schema_view import UiSchemaView
from jinja2.sandbox import SandboxedEnvironment
from plone import api

# from Products.MailHost.interfaces import IMailHost
from plone.base.utils import unrestricted_construct_instance
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.services import Service
from zExceptions import BadRequest
from zope.container.interfaces import INameChooser
from zope.interface import alsoProvides

import json
import logging
import requests


logger = logging.getLogger(__name__)


def load_form_action_data(handler_post: Service) -> str:
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

        recipient = self.request.form.get("to_address")
        if self.request.form.get("use_email_of_current_user"):
            user = api.user.get_current()
            if user and not api.user.is_anonymous():
                recipient = user.getProperty("email", default="")
            if recipient == "":
                raise BadRequest(
                    "No email was sent, because user email address is not available or no user is logged in."
                )
        # reply_to = self.request.form.get("reply_to_address", None)
        subject = self.request.form.get("subject", _("No Subject"))
        message = self.request.form.get("email_text", "") + "\n"
        message += data

        if not recipient:
            raise BadRequest("Recipient email address is required.")

        # Send email
        # self.send_email(recipient, default_sender, reply_to, subject, message)
        self.send_email(recipient, default_sender, subject, message)

        self.request.response.setStatus(200)
        return {"status": "success", "message": _("Email sent successfully.")}

    # def send_email(self, recipient, sender, reply_to_adress, subject, message):
    def send_email(self, recipient, sender, subject, message):
        """Helper method to send email."""

        # Send the email
        try:
            api.portal.send_email(
                recipient=recipient,
                sender=sender,
                subject=subject,
                body=message,
                immediate=False,
            )

        except Exception as e:
            raise BadRequest(f"Failed to send email: {e!s}") from e


class FormActionsWebserviceHandlerPost(Service):
    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        data = load_form_action_data(self)

        try:
            payload = json.loads(data)
        except json.JSONDecodeError as e:
            raise BadRequest("Invalid JSON format.") from e

        endpoints = []
        i = 1
        while True:
            url = self.request.get_header(f"endpoint-{i}-url")
            if url is None:
                break
            endpoint = {
                "url": url,
            }

            api_key_header_name = self.request.get_header(
                f"endpoint-{i}-api-key-header-name", None
            )

            # get api_key from endpoint object by extracting the endpoint's UID from the request header
            api_key = None
            endpoint_uid = self.request.get_header(f"endpoint-{i}-uid", None)
            with api.env.adopt_roles(["Manager"]):
                endpoint_obj = api.content.get(UID=endpoint_uid)
                api_key = getattr(endpoint_obj, "api_key", None)

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
                url=endpoint["url"],
                headers=headers,
                data=json.dumps(payload),
                timeout=15,
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
        except json.JSONDecodeError as e:
            raise BadRequest("Invalid JSON format.") from e

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

    def reply(self):  # noqa: C901
        alsoProvides(self.request, IDisableCSRFProtection)
        data = load_form_action_data(self)

        try:
            payload = json.loads(data)
        except json.JSONDecodeError as e:
            raise BadRequest("Invalid JSON format.") from e

        # get target folder from request form and validate it
        folder_path = self.request.form.get("folder_path")
        if not folder_path:
            raise BadRequest("Folder path is required.")
        with api.env.adopt_roles(["Manager"]):
            folder = api.content.get(path=folder_path)
        if folder is None:
            raise BadRequest("Folder path is invalid.")

        # get content object title from request form, validate it and render it as
        # jinja2 template with form data as variables
        content_object_title = self.request.form.get(
            "content_object_title", _("Form submission")
        )
        env = SandboxedEnvironment()
        try:
            obj_title = env.from_string(content_object_title).render(
                data=payload,
                user=api.user.get_current().getUserId()
                if api.user.get_current() and not api.user.is_anonymous()
                else "anonymous",
            )
        except Exception as e:
            logging.error(f"Error rendering content object title template: {e}")
            obj_title = _("Form submission")

        if not obj_title or obj_title.isspace():
            obj_title = _("Form submission")

        # create JsonFormsDocument inside the target folder but bypass checks (don't
        # use api.content.create)
        with api.env.adopt_roles(["Manager"]):
            container = api.content.get(path=folder_path)
            if container is None:
                logging.error(f"Container not found at path: {folder_path}")
                raise BadRequest("Container not found at specified folder path.")

            chooser = INameChooser(container)
            new_id = chooser.chooseName(obj_title, container)  # create unique id
            try:
                jsonformsdocument = unrestricted_construct_instance(
                    "JsonFormsDocument", container, new_id, title=obj_title
                )
            except Exception as e:
                logging.error(f"Error creating JsonFormsDocument: {e}")
                raise BadRequest("Error creating content object.") from e

        # set fields of the created object
        jsonformsdocument.json_data = json.dumps(payload, ensure_ascii=False, indent=4)
        jsonformsdocument.json_schema = JsonSchemaView(self.context, self.request)()
        ui_schema = json.loads(UiSchemaView(self.context, self.request)())
        # remove all buttongroups
        try:
            new_list = []
            for element in ui_schema.get("layout", []).get("elements", []):
                if element.get("type") == "Buttongroup":
                    continue
                else:
                    new_list.append(element)
            ui_schema["layout"]["elements"] = new_list
            # put new buttongroup into the ui schema to enable editing the
            # created JsonFormsDocument
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
                                    "url": f"{jsonformsdocument.absolute_url()}/@edit-jsonformsdocument",  # noqa: E501
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
        except Exception as e:
            logging.error(f"Error processing UI schema: {e}")
            raise BadRequest("Error processing UI schema.") from e

        # set state to private so only admins and the creator can see the created object
        # bypass permission checks to make transition also as anonymous user
        with api.env.adopt_roles(["Manager"]):
            try:
                api.content.transition(obj=jsonformsdocument, transition="hide")
                if api.content.get_state(jsonformsdocument) != "private":
                    api.content.transition(obj=jsonformsdocument, to_state="private")
            except Exception as e:
                logging.debug(
                    "Failed to transition JsonFormsDocument to 'private' state: %s", e
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
    """
    Endpoint to edit a JsonFormsDocument created by the FormActionsFileStorageHandler
    """

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        data = load_form_action_data(self)

        try:
            payload = json.loads(data)
        except json.JSONDecodeError as e:
            raise BadRequest("Invalid JSON format.") from e

        # check that self.context was created by the current user
        # if user is anonymous, content cannot be edited
        user = api.user.get_current()
        if not user:
            raise BadRequest("Anonymous users cannot edit content.")
        if self.context.Creator() != user.getUserId() and not api.user.has_permission(
            "Modify portal content", obj=self.context
        ):
            raise BadRequest("You can only edit content created by yourself.")
        # update json_data field of the context JsonFormsDocument with the new data
        self.context.json_data = json.dumps(payload, ensure_ascii=False, indent=4)

        self.request.response.setStatus(200)
        return {"status": "success", "message": _("Data updated successfully.")}
