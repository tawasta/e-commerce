from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class CustomerPortalEdicode(CustomerPortal):
    def __init__(self):
        super().__init__()
        self.OPTIONAL_BILLING_FIELDS.extend(["einvoice_operator_id", "edicode"])

    def details_form_validate(self, data, partner_creation=False):
        error, error_message = super().details_form_validate(data, partner_creation)

        if data.get("einvoice_operator_id"):
            data["einvoice_operator_id"] = int(data["einvoice_operator_id"])
        if data.get("edicode"):
            data["edicode"] = data["edicode"]
        return error, error_message
