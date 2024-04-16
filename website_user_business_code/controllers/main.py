from odoo import _
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.exceptions import ValidationError
from odoo.http import request


class CustomerPortalBusinessCode(CustomerPortal):
    def __init__(self):
        super(CustomerPortalBusinessCode, self).__init__()

        self.OPTIONAL_BILLING_FIELDS = self.OPTIONAL_BILLING_FIELDS + [
            "company_registry"
        ]

    def details_form_validate(self, data):
        error, error_message = super(
            CustomerPortalBusinessCode, self
        ).details_form_validate(data)

        # Business id validation
        if data.get("company_registry"):
            try:
                # Try writing the value
                # TODO: This will bypass rollback on invalid data
                partner = request.env.user.partner_id
                partner.company_registry = data["company_registry"]

            except ValidationError:
                error["company_registry"] = "error"

                # Don't use the ValidationError-message (wrong format)
                error_message.append(_("Invalid business id."))

        return error, error_message
