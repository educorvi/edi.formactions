# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Item
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

    from_address = schema.TextLine(title=_('From address'),
                                   description=_('The email address of the sender'),
                                   required=False)
    
    to_address = schema.TextLine(title=_('To address'),
                                   description=_('The email address of the recipient'),
                                   required=True)
    
    subject = schema.TextLine(title=_('Subject'),
                                   description=_('The subject of the email'),
                                   required=False)
    
    email_text = schema.Text(title=_('Email Body'),
                                 required=False)
    
    button_label = schema.TextLine(title=_('Label of the button'),
                                   description=_('What is displayed inside the button.'),
                                   required=True,
                                   default="Send email")


    # directives.widget(level=RadioFieldWidget)
    # level = schema.Choice(
    #     title=_(u'Sponsoring Level'),
    #     vocabulary=LevelVocabulary,
    #     required=True
    # )

    # text = RichText(
    #     title=_(u'Text'),
    #     required=False
    # )

    # url = schema.URI(
    #     title=_(u'Link'),
    #     required=False
    # )

    # fieldset('Images', fields=['logo', 'advertisement'])
    # logo = namedfile.NamedBlobImage(
    #     title=_(u'Logo'),
    #     required=False,
    # )

    # advertisement = namedfile.NamedBlobImage(
    #     title=_(u'Advertisement (Gold-sponsors and above)'),
    #     required=False,
    # )

    # directives.read_permission(notes='cmf.ManagePortal')
    # directives.write_permission(notes='cmf.ManagePortal')
    # notes = RichText(
    #     title=_(u'Secret Notes (only for site-admins)'),
    #     required=False
    # )


@implementer(IEmailHandler)
class EmailHandler(Item):
    """ Content-type class for IEmailHandler
    """
