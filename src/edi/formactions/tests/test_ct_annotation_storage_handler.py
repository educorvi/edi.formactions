# -*- coding: utf-8 -*-
from edi.formactions.content.annotation_storage_handler import IAnnotationStorageHandler  # NOQA E501
from edi.formactions.testing import EDI_FORMACTIONS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class AnnotationStorageHandlerIntegrationTest(unittest.TestCase):
    layer = EDI_FORMACTIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            "Button",
            self.portal,
            "parent_container",
            title="Parent container",
        )
        self.parent = self.portal[parent_id]

    def test_ct_annotation_storage_handler_schema(self):
        fti = queryUtility(IDexterityFTI, name="Annotation Storage Handler")
        schema = fti.lookupSchema()
        self.assertEqual(IAnnotationStorageHandler, schema)

    def test_ct_annotation_storage_handler_fti(self):
        fti = queryUtility(IDexterityFTI, name="Annotation Storage Handler")
        self.assertTrue(fti)

    def test_ct_annotation_storage_handler_factory(self):
        fti = queryUtility(IDexterityFTI, name="Annotation Storage Handler")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IAnnotationStorageHandler.providedBy(obj),
            "IAnnotationStorageHandler not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_annotation_storage_handler_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.parent,
            type="Annotation Storage Handler",
            id="annotation_storage_handler",
        )

        self.assertTrue(
            IAnnotationStorageHandler.providedBy(obj),
            "IAnnotationStorageHandler not provided by {0}!".format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn("annotation_storage_handler", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("annotation_storage_handler", parent.objectIds())

    def test_ct_annotation_storage_handler_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Annotation Storage Handler")
        self.assertFalse(fti.global_allow, "{0} is globally addable!".format(fti.id))

    def test_ct_annotation_storage_handler_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Annotation Storage Handler")
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            "annotation_storage_handler_id",
            title="Annotation Storage Handler container",
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type="Document",
                title="My Content",
            )
