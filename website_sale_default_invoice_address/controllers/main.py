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
            # Check if partner has a default invoice address
            order.partner_invoice_id = order.partner_id.default_partner_invoice_id
        elif order.commercial_partner_id.default_partner_invoice_id:
            # Check if commercial partner has a default invoice address
            order.partner_invoice_id = (
                order.commercial_partner_id.default_partner_invoice_id
            )

        return super().checkout(**post)
