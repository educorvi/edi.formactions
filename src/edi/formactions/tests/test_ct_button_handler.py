# -*- coding: utf-8 -*-
from edi.formactions.content.button_handler import IButtonHandler  # NOQA E501
from edi.formactions.testing import EDI_FORMACTIONS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class ButtonHandlerIntegrationTest(unittest.TestCase):

    layer = EDI_FORMACTIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_button_handler_schema(self):
        fti = queryUtility(IDexterityFTI, name='Button Handler')
        schema = fti.lookupSchema()
        self.assertEqual(IButtonHandler, schema)

    def test_ct_button_handler_fti(self):
        fti = queryUtility(IDexterityFTI, name='Button Handler')
        self.assertTrue(fti)

    def test_ct_button_handler_factory(self):
        fti = queryUtility(IDexterityFTI, name='Button Handler')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IButtonHandler.providedBy(obj),
            u'IButtonHandler not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_button_handler_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Button Handler',
            id='button_handler',
        )

        self.assertTrue(
            IButtonHandler.providedBy(obj),
            u'IButtonHandler not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('button_handler', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('button_handler', parent.objectIds())

    def test_ct_button_handler_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Button Handler')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_button_handler_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Button Handler')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'button_handler_id',
            title='Button Handler container',
        )
        self.parent = self.portal[parent_id]
        obj = api.content.create(
            container=self.parent,
            type='Document',
            title='My Content',
        )
        self.assertTrue(
            obj,
            u'Cannot add {0} to {1} container!'.format(obj.id, fti.id)
        )
