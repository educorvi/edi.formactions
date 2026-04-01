from edi.formactions.testing import EDI_FORMACTIONS_ACCEPTANCE_TESTING
from edi.formactions.testing import EDI_FORMACTIONS_FUNCTIONAL_TESTING
from edi.formactions.testing import EDI_FORMACTIONS_INTEGRATION_TESTING
from pytest_plone import fixtures_factory


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory((
        (EDI_FORMACTIONS_ACCEPTANCE_TESTING, "acceptance"),
        (EDI_FORMACTIONS_FUNCTIONAL_TESTING, "functional"),
        (EDI_FORMACTIONS_INTEGRATION_TESTING, "integration"),
    ))
)
