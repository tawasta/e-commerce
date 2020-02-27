from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleProduct(WebsiteSale):
    @http.route()
    def product(self, product, category="", search="", **kwargs):

        res = super(WebsiteSaleProduct, self).product(
            product, category, search, **kwargs
        )

        res.qcontext["website_product_description"] = product.description

        return res
