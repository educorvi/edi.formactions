# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Container
# from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer


from edi.formactions import _


class IResetButton(model.Schema):
    """ Marker interface and Dexterity Python Schema for ResetButton
    """

    button_label = schema.TextLine(title=_('Label of the button'),
                                   description=_('What is displayed inside the button.'),
                                   required=True,
                                   default=_("Reset form"))
    button_variant = schema.Choice(title=_('Color variant of the button'),
                                   description=_('The color variant of the button.'),
                                   required=True,
                                   default='danger',
                                   vocabulary='plone.app.widgets.buttons:BUTTON_VARIANTS')

@implementer(IResetButton)
class ResetButton(Container):
    """ Content-type class for IResetButton
    """
