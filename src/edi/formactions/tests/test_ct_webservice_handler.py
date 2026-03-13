# -*- coding: utf-8 -*-
from edi.formactions.content.webservice_handler import IWebserviceHandler  # NOQA E501
from edi.formactions.testing import EDI_FORMACTIONS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class WebserviceHandlerIntegrationTest(unittest.TestCase):

    layer = EDI_FORMACTIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'Button',
            self.portal,
            'parent_container',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_webservice_handler_schema(self):
        fti = queryUtility(IDexterityFTI, name='Webservice Handler')
        schema = fti.lookupSchema()
        self.assertEqual(IWebserviceHandler, schema)

    def test_ct_webservice_handler_fti(self):
        fti = queryUtility(IDexterityFTI, name='Webservice Handler')
        self.assertTrue(fti)

    def test_ct_webservice_handler_factory(self):
        fti = queryUtility(IDexterityFTI, name='Webservice Handler')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IWebserviceHandler.providedBy(obj),
            u'IWebserviceHandler not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_webservice_handler_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='Webservice Handler',
            id='webservice_handler',
        )

        self.assertTrue(
            IWebserviceHandler.providedBy(obj),
            u'IWebserviceHandler not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('webservice_handler', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('webservice_handler', parent.objectIds())

    def test_ct_webservice_handler_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Webservice Handler')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )

    def test_ct_webservice_handler_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Webservice Handler')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'webservice_handler_id',
            title='Webservice Handler container',
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
