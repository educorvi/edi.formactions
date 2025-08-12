# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zExceptions import BadRequest
from zope.component import getUtility
from Products.MailHost.interfaces import IMailHost
from plone.api import portal
from plone.base.utils import safe_text
import requests

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import json

from edi.formactions import _


# @implementer(IExpandableElement)
# @adapter(Interface, Interface)
# class FormActions(object):

#     def __init__(self, context, request):
#         self.context = context.aq_explicit
#         self.request = request

#     def __call__(self, expand=False):
#         result = {
#             'form_actions': {
#                 '@id': '{}/@form_actions'.format(
#                     self.context.absolute_url(),
#                 ),
#             },
#         }
#         if not expand:
#             return result

#         # === Your custom code comes here ===

#         # Example:
#         try:
#             subjects = self.context.Subject()
#         except Exception as e:
#             print(e)
#             subjects = []
#         query = {}
#         query['portal_type'] = "Document"
#         query['Subject'] = {
#             'query': subjects,
#             'operator': 'or',
#         }
#         brains = api.content.find(**query)
#         items = []
#         for brain in brains:
#             # obj = brain.getObject()
#             # parent = obj.aq_inner.aq_parent
#             items.append({
#                 'title': brain.Title,
#                 'description': brain.Description,
#                 '@id': brain.getURL(),
#             })
#         result['form_actions']['items'] = items
#         return result


class FormActionsEmailHandlerPost(Service):

    default_sender = 'noreply@plone.org'

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

        recipient = self.request.form.get('to_address')
        reply_to = self.request.form.get('reply_to_address', None)
        subject = self.request.form.get('subject', _('No Subject'))
        message = self.request.form.get('email_text', '') + '\n'

        message += data

        if not recipient:
            raise BadRequest("Recipient email address is required.")

        # Send email
        response = self.send_email(recipient, self.default_sender, reply_to, subject, message)

        self.request.response.setStatus(200)
        return response
    
    def send_email(self, recipient, sender, reply_to_adress, subject, message):
        """Helper method to send email."""
        # Get the MailHost utility
        # mail_host = getUtility(IMailHost)
        mail_host = portal.get_tool(name='MailHost')
        
        # Construct the email
        # portal_obj = portal.get()
        # sender = portal_obj.getProperty('email_from_address')
        # if not sender:
        #     raise ValueError("Portal email_from_address is not set.")
        
        subject = safe_text(subject)

        messageText = MIMEMultipart()
        messageText.attach(MIMEText(message, 'plain', 'utf-8'))
        if reply_to_adress:
            messageText['Reply-To'] = reply_to_adress
        
        # Send the email
        try:
            return mail_host.send(
                messageText=messageText,
                mto=recipient,
                mfrom=sender,
                subject=subject,
                charset='utf-8',
                immediate=True
            )
            # portal.send_email(
            #     recipient=recipient,
            #     subject=subject,
            #     body=message_body
            # )
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
