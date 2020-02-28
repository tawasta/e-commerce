from odoo.addons.portal.controllers.portal import CustomerPortal


class Portal(CustomerPortal):

    def __init__(self):
        super(Portal, self).__init__()

        self.OPTIONAL_BILLING_FIELDS += ['property_product_pricelist']
