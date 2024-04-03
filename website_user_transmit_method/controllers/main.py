from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    def __init__(self):
        super().__init__()
        self.OPTIONAL_BILLING_FIELDS.extend(["customer_invoice_transmit_method_id"])

    def details_form_validate(self, data, partner_creation=False):
        error, error_message = super().details_form_validate(data, partner_creation)

        if data.get('customer_invoice_transmit_method_id'):
            data['customer_invoice_transmit_method_id'] = int(data['customer_invoice_transmit_method_id'])
        return error, error_message
