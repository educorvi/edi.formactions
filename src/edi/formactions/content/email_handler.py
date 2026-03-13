# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Container

# from plone.namedfile import field as namedfile
from plone.supermodel import model

# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer, invariant, Invalid


from edi.formactions import _
from edi.formactions.content.generic_handler import IGenericHandler, GenericHandler


class IEmailHandler(IGenericHandler):
    """Marker interface and Dexterity Python Schema for EmailHandler"""

    use_email_of_current_user = schema.Bool(
        title=_("Use email of current user as recipient"),
        description=_(
            "If checked, the email address of the current user will be used instead of the 'To address' field."
        ),
        required=False,
        default=False,
    )

    to_address = schema.TextLine(
        title=_("To address"),
        description=_(
            "The email address of the recipient. This field is required if 'Use email of current user as recipient' is not checked."
        ),
        required=False,
    )

    # reply_to_address = schema.TextLine(
    #     title=_("Reply-to address"),
    #     description=_("The email address to which replies should be sent."),
    #     required=False,
    # )

    email_subject = schema.TextLine(
        title=_("Subject"), description=_("The subject of the email."), required=False
    )

    email_text = schema.Text(
        title=_("Email Body"),
        description=_(
            "The body of the email. The content of the form will be appended to this text."
        ),
        required=False,
    )

    @invariant
    def validate_to_address(data):
        if not data.use_email_of_current_user and not data.to_address:
            raise Invalid(
                _(
                    "To address is required if 'Use email of current user as recipient' is not checked."
                )
            )
        if data.use_email_of_current_user and data.to_address:
            raise Invalid(
                _(
                    "To address should not be set if 'Use email of current user as recipient' is checked."
                )
            )


@implementer(IEmailHandler)
class EmailHandler(GenericHandler):
    """Content-type class for IEmailHandler"""
