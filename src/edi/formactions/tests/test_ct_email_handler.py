# -*- coding: utf-8 -*-
from edi.formactions.content.email_handler import IEmailHandler  # NOQA E501
from edi.formactions.testing import EDI_FORMACTIONS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class EmailHandlerIntegrationTest(unittest.TestCase):

    layer = EDI_FORMACTIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'Button Handler',
            self.portal,
            'parent_container',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_email_handler_schema(self):
        fti = queryUtility(IDexterityFTI, name='Email Handler')
        schema = fti.lookupSchema()
        self.assertEqual(IEmailHandler, schema)

    def test_ct_email_handler_fti(self):
        fti = queryUtility(IDexterityFTI, name='Email Handler')
        self.assertTrue(fti)

    def test_ct_email_handler_factory(self):
        fti = queryUtility(IDexterityFTI, name='Email Handler')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IEmailHandler.providedBy(obj),
            u'IEmailHandler not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_email_handler_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='Email Handler',
            id='email_handler',
        )

        self.assertTrue(
            IEmailHandler.providedBy(obj),
            u'IEmailHandler not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('email_handler', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('email_handler', parent.objectIds())

    def test_ct_email_handler_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Email Handler')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )
