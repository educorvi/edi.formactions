# -*- coding: utf-8 -*-
from edi.formactions.content.json_forms_document import IJsonFormsDocument  # NOQA E501
from edi.formactions.testing import EDI_FORMACTIONS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class JsonFormsDocumentIntegrationTest(unittest.TestCase):
    layer = EDI_FORMACTIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.parent = self.portal

    def test_ct_json_forms_document_schema(self):
        fti = queryUtility(IDexterityFTI, name="JsonFormsDocument")
        schema = fti.lookupSchema()
        self.assertEqual(IJsonFormsDocument, schema)

    def test_ct_json_forms_document_fti(self):
        fti = queryUtility(IDexterityFTI, name="JsonFormsDocument")
        self.assertTrue(fti)

    def test_ct_json_forms_document_factory(self):
        fti = queryUtility(IDexterityFTI, name="JsonFormsDocument")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IJsonFormsDocument.providedBy(obj),
            "IJsonFormsDocument not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_json_forms_document_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.portal,
            type="JsonFormsDocument",
            id="json_forms_document",
        )

        self.assertTrue(
            IJsonFormsDocument.providedBy(obj),
            "IJsonFormsDocument not provided by {0}!".format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn("json_forms_document", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("json_forms_document", parent.objectIds())

    def test_ct_json_forms_document_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="JsonFormsDocument")
        self.assertFalse(fti.global_allow, "{0} is globally addable!".format(fti.id))

    def test_ct_json_forms_document_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="JsonFormsDocument")
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            "json_forms_document_id",
            title="JsonFormsDocument container",
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type="Document",
                title="My Content",
            )
