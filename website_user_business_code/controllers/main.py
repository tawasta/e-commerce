from odoo import _
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.exceptions import ValidationError
from odoo.http import request


class CustomerPortalBusinessCode(CustomerPortal):

    def __init__(self):
        super(CustomerPortal, self).__init__()

        self.OPTIONAL_BILLING_FIELDS = \
            self.OPTIONAL_BILLING_FIELDS + ['business_id']

    def details_form_validate(self, data):
        error, error_message = super(CustomerPortalBusinessCode, self)\
            .details_form_validate(data)

        # Business id validation
        if data.get('business_id'):
            id_category = request.env['res.partner.id_category']

            if hasattr(id_category, 'validate_business_id'):
                # Check if validation method exists and run it, if necessary
                try:
                    # Try writing the value
                    # TODO: This will bypass rollback on invalid data
                    partner = request.env.user.partner_id
                    partner.business_id = data['business_id']

                except ValidationError:
                    error["business_id"] = 'error'

                    # Don't use the ValidationError-message (wrong format)
                    error_message.append(
                        _("Invalid business id.")
                    )

        return error, error_message
