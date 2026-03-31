from . import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


BOOTSTRAP_BUTTON_VARIANTS = [
    ("primary", _("Primary")),
    ("secondary", _("Secondary")),
    ("success", _("Success")),
    ("danger", _("Danger")),
    ("warning", _("Warning")),
    ("outline-primary", _("Primary Outline")),
    ("outline-secondary", _("Secondary Outline")),
    ("outline-success", _("Success Outline")),
    ("outline-danger", _("Danger Outline")),
    ("outline-warning", _("Warning Outline")),
    ("info", _("Info")),
    ("light", _("Light")),
    ("dark", _("Dark")),
]


@implementer(IVocabularyFactory)
class ButtonVariantsVocabulary:
    """Vocabulary factory for Bootstrap button variants.

    Provides terms suitable for use in a Choice field.
    Values and tokens are the raw variant keys (e.g. "primary").
    Titles are translated human-readable labels.
    """

    def __call__(self, context):
        terms = [
            SimpleTerm(value=key, token=key, title=title)
            for key, title in BOOTSTRAP_BUTTON_VARIANTS
        ]
        return SimpleVocabulary(terms)
