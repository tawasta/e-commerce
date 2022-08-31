from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleDefaultInvoiceAddress(WebsiteSale):
    @http.route()
    def checkout(self, **post):
        """
        Set the default invoice address, if applicable
        """

        order = request.website.sale_get_order()

        if order.partner_id.default_partner_invoice_id:
            order.partner_invoice_id = order.partner_id.default_partner_invoice_id

        return super().checkout(**post)
