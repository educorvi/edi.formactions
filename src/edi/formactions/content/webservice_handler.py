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


class IWebserviceHandler(model.Schema):
    """ Marker interface and Dexterity Python Schema for WebserviceHandler
    """
    button_label = schema.TextLine(title=_('Label of the button'),
                                   description=_('What is displayed inside the button.'),
                                   required=True,
                                   default=_("Send request(s)"))

    button_variant = schema.Choice(title=_('Color variant of the button'),
                                   description=_('The color variant of the button.'),
                                   required=True,
                                   default='primary',
                                   vocabulary='plone.app.widgets.buttons:BUTTON_VARIANTS')

    page_after_success = schema.URI(
        title=_('Page after success'),
        description=_('The page to redirect to after a successful request.'),
        required=False,
        default='about:blank',
    )


@implementer(IWebserviceHandler)
class WebserviceHandler(Container):
    """ Content-type class for IWebserviceHandler
    """
