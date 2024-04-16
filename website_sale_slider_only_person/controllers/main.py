from odoo import http

from odoo.addons.tivia_website_sale.controllers.main import WebsiteSaleCustom


class WebsiteSaleContact(WebsiteSaleCustom):
    @http.route(
        ["/shop/cart/check_company_membership"],
        type="json",
        auth="public",
        website=True,
    )
    def check_company_membership(self):
        return {"membership_status": "contact"}
