# -*- coding: utf-8 -*-
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from . import _


BOOTSTRAP_BUTTON_VARIANTS = [
    ("primary", _(u"Primary")),
    ("secondary", _(u"Secondary")),
    ("success", _(u"Success")),
    ("danger", _(u"Danger")),
    ("warning", _(u"Warning")),
    ("outline-primary", _(u"Primary Outline")),
    ("outline-secondary", _(u"Secondary Outline")),
    ("outline-success", _(u"Success Outline")),
    ("outline-danger", _(u"Danger Outline")),
    ("outline-warning", _(u"Warning Outline")),
    ("info", _(u"Info")),
    ("light", _(u"Light")),
    ("dark", _(u"Dark")),
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
            SimpleTerm(value=key, token=key, title=title) for key, title in BOOTSTRAP_BUTTON_VARIANTS
        ]
        return SimpleVocabulary(terms)
