from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    def __init__(self):
        super(CustomerPortal, self).__init__()

        self.OPTIONAL_BILLING_FIELDS = \
            self.OPTIONAL_BILLING_FIELDS + \
            ['customer_invoice_transmit_method_id']
