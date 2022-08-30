from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleForceAddress(WebsiteSale):
    @http.route()
    def checkout(self, **post):
        post.pop("express")

        return super().checkout(**post)
