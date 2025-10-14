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
from plone.base.utils import safe_text
from plone.protect.interfaces import IDisableCSRFProtection
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from edi.formactions import _

class FormActionsEmailHandlerPost(Service):

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        default_sender = api.portal.get_registry_record('plone.email_from_address', default='noreply@plone.org')
        data = self.request.get('BODY', None)
        if not data:
            raise BadRequest("No data provided.")

        if isinstance(data, bytes):
            data = data.decode('utf-8')

        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            raise BadRequest("Invalid JSON format.")

        recipient = self.request.form.get('to_address')
        reply_to = self.request.form.get('reply_to_address', None)
        subject = self.request.form.get('subject', _('No Subject'))
        message = self.request.form.get('email_text', '') + '\n'

        message += data

        if not recipient:
            raise BadRequest("Recipient email address is required.")

        # Send email
        response = self.send_email(recipient, default_sender, reply_to, subject, message)

        self.request.response.setStatus(200)
        return response

    def send_email(self, recipient, sender, reply_to_adress, subject, message):
        """Helper method to send email."""

        messageText = MIMEMultipart()
        messageText.attach(MIMEText(message, 'plain', 'utf-8'))
        messageText["Subject"] = subject
        if reply_to_adress:
            messageText['Reply-To'] = reply_to_adress

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
        data = self.request.get('BODY', None)
        if not data:
            raise BadRequest("No data provided.")

        if isinstance(data, bytes):
            data = data.decode('utf-8')

        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            raise BadRequest("Invalid JSON format.")

        endpoints = []
        i = 1
        while True:
            if f'endpoint_{i}_url' not in self.request.form:
                break
            url = self.request.form.get(f'endpoint_{i}_url')
            endpoint = {
                'url': url,
            }
            api_key_header_name = self.request.form.get(f'endpoint_{i}_api_key_header_name', None)
            api_key = self.request.form.get(f'endpoint_{i}_api_key', None)
            if api_key_header_name and api_key:
                endpoint[api_key_header_name] = api_key
            endpoints.append(endpoint)
            i += 1

        page_after_success = self.request.form.get('page_after_success', None)

        self.request.response.setStatus(200)
        status = 'success'
        message = _('Web service request sent successfully.')
        error_message = _('Error sending request to: ')
        error_occurred = False
        for endpoint in endpoints:
            headers={k: v for k, v in endpoint.items() if k != 'url'}
            headers['Referer'] = "https://plone.org" # self.context.absolute_url()
            response = requests.post(url=endpoint['url'],
                                     headers=headers,
                                     data=json.dumps(payload)
            )

            if response.status_code != 200:
                error_occurred = True
                self.request.response.setStatus(400)
                status = 'error'
                error_message += f"{endpoint['url']}: {response.text}, "

        if error_occurred:
            api.portal.show_message(message=error_message, request=self.request, type='error')
        elif page_after_success:
            self.request.response.redirect(page_after_success)
        else:
            return {'status': status, 'message': message}
