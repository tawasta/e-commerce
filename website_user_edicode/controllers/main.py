from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalEdicode(CustomerPortal):

    def __init__(self):
        super(CustomerPortal, self).__init__()

        self.OPTIONAL_BILLING_FIELDS = \
            self.OPTIONAL_BILLING_FIELDS + ['edicode', 'einvoice_operator']
