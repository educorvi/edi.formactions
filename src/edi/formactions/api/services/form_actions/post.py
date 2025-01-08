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
from Products.CMFPlone.utils import safe_unicode

import json


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

    def reply(self):
        print("hallo")
        data = self.request.get('BODY', None)
        if not data:
            raise BadRequest("No data provided.")
        
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        
        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            raise BadRequest("Invalid JSON format.")
        
        # Extract the required fields from the payload
        recipient = payload.get('recipient')    # TODO enter correct location in json
        sender = payload.get('sender', 'ninamuecke@gmx.com')
        subject = payload.get('subject', 'No Subject')
        message = payload.get('message', 'No Message')
        message += "\n" + data

        if not recipient:
            raise BadRequest("Recipient email address is required.")

        # Send email
        self.send_email(recipient, sender, subject, message)

        self.request.response.setStatus(201)
        print("yay")
        return {
            'text': 'IT WORKS!',
            'sent data': data
        }
    
    def send_email(self, recipient, sender, subject, message):
        """Helper method to send email."""
        # Get the MailHost utility
        mail_host = getUtility(IMailHost)
        import pdb; pdb.set_trace()
        
        # Construct the email
        # portal_obj = portal.get()
        # sender = portal_obj.getProperty('email_from_address')
        # if not sender:
        #     raise ValueError("Portal email_from_address is not set.")
        
        subject = safe_unicode(subject)
        message_body = f"Subject: {subject}\n\n{message}"
        
        # Send the email
        try:
            mail_host.send(
                message_body,
                recipient,
                sender,
                subject=subject,
                charset='utf-8',
            )
        except Exception as e:
            raise BadRequest(f"Failed to send email: {str(e)}")
        
