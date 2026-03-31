from edi.formactions.content.endpoint import IEndpoint
from edi.formactions.testing import EDI_FORMACTIONS_INTEGRATION_TESTING
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class EndpointIntegrationTest(unittest.TestCase):
    layer = EDI_FORMACTIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            "Webservice Handler",
            self.portal,
            "parent_container",
            title="Parent container",
        )
        self.parent = self.portal[parent_id]

    def test_ct_endpoint_schema(self):
        fti = queryUtility(IDexterityFTI, name="Endpoint")
        schema = fti.lookupSchema()
        self.assertEqual(IEndpoint, schema)

    def test_ct_endpoint_fti(self):
        fti = queryUtility(IDexterityFTI, name="Endpoint")
        self.assertTrue(fti)

    def test_ct_endpoint_factory(self):
        fti = queryUtility(IDexterityFTI, name="Endpoint")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IEndpoint.providedBy(obj),
            f"IEndpoint not provided by {obj}!",
        )

    def test_ct_endpoint_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.parent,
            type="Endpoint",
            id="endpoint",
        )

        self.assertTrue(
            IEndpoint.providedBy(obj),
            f"IEndpoint not provided by {obj.id}!",
        )

        parent = obj.__parent__
        self.assertIn("endpoint", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("endpoint", parent.objectIds())

    def test_ct_endpoint_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Endpoint")
        self.assertFalse(fti.global_allow, f"{fti.id} is globally addable!")

    def test_ct_endpoint_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Endpoint")
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            "endpoint_id",
            title="Endpoint container",
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type="Document",
                title="My Content",
            )
