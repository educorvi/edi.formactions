# -*- coding: utf-8 -*-
from edi.formactions.testing import EDI_FORMACTIONS_FUNCTIONAL_TESTING
from edi.formactions.testing import EDI_FORMACTIONS_INTEGRATION_TESTING
from edi.formactions.views.json_forms_document_view import IJsonFormsDocumentView
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = EDI_FORMACTIONS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Folder', 'other-folder')
        api.content.create(self.portal, 'Document', 'front-page')

    def test_json_forms_document_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='json-forms-document-view'
        )
        self.assertTrue(IJsonFormsDocumentView.providedBy(view))

    def test_json_forms_document_view_not_matching_interface(self):
        view_found = True
        try:
            view = getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='json-forms-document-view'
            )
        except ComponentLookupError:
            view_found = False
        else:
            view_found = IJsonFormsDocumentView.providedBy(view)
        self.assertFalse(view_found)


class ViewsFunctionalTest(unittest.TestCase):

    layer = EDI_FORMACTIONS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
