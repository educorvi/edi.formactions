# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zExceptions import BadRequest


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
        data = self.request.get('BODY', None)
        if not data:
            raise BadRequest("No data provided.")
        
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        
        # TODO process data to send email

        self.request.response.setStatus(201)
        print("yay")
        return {
            'text': 'IT WORKS!',
            'sent data': data
        }
        
