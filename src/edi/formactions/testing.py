# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import edi.formactions


class EdiFormactionsLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=edi.formactions)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "edi.formactions:default")


EDI_FORMACTIONS_FIXTURE = EdiFormactionsLayer()


EDI_FORMACTIONS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EDI_FORMACTIONS_FIXTURE,),
    name="EdiFormactionsLayer:IntegrationTesting",
)


EDI_FORMACTIONS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EDI_FORMACTIONS_FIXTURE,),
    name="EdiFormactionsLayer:FunctionalTesting",
)


EDI_FORMACTIONS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EDI_FORMACTIONS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="EdiFormactionsLayer:AcceptanceTesting",
)
