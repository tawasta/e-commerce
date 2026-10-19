from odoo.http import route

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleForceAddressStep(WebsiteSale):
    @route()
    def shop_checkout(self, try_skip_step=None, **query_params):
        # Never auto-skip the checkout page: customers always review their
        # addresses, even for carts without deliverable products.
        return super().shop_checkout(try_skip_step=False, **query_params)
