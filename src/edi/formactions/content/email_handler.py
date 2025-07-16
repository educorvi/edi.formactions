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


class IEmailHandler(model.Schema):
    """ Marker interface and Dexterity Python Schema for EmailHandler
    """
    # If you want, you can load a xml model created TTW here
    # and customize it in Python:
    
    to_address = schema.TextLine(title=_('To address'),
                                   description=_('The email address of the recipient'),
                                   required=True)
    
    reply_to_address = schema.TextLine(title=_('Reply-to address'),
                                       description=_('The email address to which replies should be sent.'),
                                       required=False)
    
    email_subject = schema.TextLine(title=_('Subject'),
                                   description=_('The subject of the email.'),
                                   required=False)
    
    email_text = schema.Text(title=_('Email Body'),
                             description=_('The body of the email. The content of the form will be appended to this text.'),
                             required=False)
    
    button_label = schema.TextLine(title=_('Label of the button'),
                                   description=_('What is displayed inside the button.'),
                                   required=True,
                                   default="Send email")




@implementer(IEmailHandler)
class EmailHandler(Container):
    """ Content-type class for IEmailHandler
    """
