from edi.formactions.content.button_group import IButtonGroup
from edi.formactions.testing import EDI_FORMACTIONS_INTEGRATION_TESTING
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class ButtonGroupIntegrationTest(unittest.TestCase):
    layer = EDI_FORMACTIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            "Form",
            self.portal,
            "parent_container",
            title="Parent container",
        )
        self.parent = self.portal[parent_id]

    def test_ct_button_group_schema(self):
        fti = queryUtility(IDexterityFTI, name="Button Group")
        schema = fti.lookupSchema()
        self.assertEqual(IButtonGroup, schema)

    def test_ct_button_group_fti(self):
        fti = queryUtility(IDexterityFTI, name="Button Group")
        self.assertTrue(fti)

    def test_ct_button_group_factory(self):
        fti = queryUtility(IDexterityFTI, name="Button Group")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IButtonGroup.providedBy(obj),
            f"IButtonGroup not provided by {obj}!",
        )

    def test_ct_button_group_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.parent,
            type="Button Group",
            id="button_group",
        )

        self.assertTrue(
            IButtonGroup.providedBy(obj),
            f"IButtonGroup not provided by {obj.id}!",
        )

        parent = obj.__parent__
        self.assertIn("button_group", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("button_group", parent.objectIds())

    def test_ct_button_group_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Button Group")
        self.assertFalse(fti.global_allow, f"{fti.id} is globally addable!")

    def test_ct_button_group_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Button Group")
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            "button_group_id",
            title="Button Group container",
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type="Document",
                title="My Content",
            )
