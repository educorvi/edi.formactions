from plone.supermodel import model
from plone.dexterity.content import Container
from zope import schema
from zope import schema
from zope.interface import implementer
from edi.formactions import _

class IGenericHandler(model.Schema):
    """ Marker interface and Dexterity Python Schema for GenericHandler
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
    )


@implementer(IGenericHandler)
class GenericHandler(Container):
    """ Content-type class for IGenericHandler
    """
