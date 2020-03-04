# from odoo.addons.website_portal.controllers.main import website_account
from odoo import website_account


class CustomerPortal(website_account):

    def __init__(self):
        super(CustomerPortal, self).__init__()

        self.OPTIONAL_BILLING_FIELDS = \
            self.OPTIONAL_BILLING_FIELDS + ['edicode', 'einvoice_operator']
