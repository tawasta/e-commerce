from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class CheckoutSkipPaymentAndConfirmation(WebsiteSale):

    @http.route()
    def payment_confirmation(self, **post):
        if not request.website.checkout_skip_payment:
            return super().payment_confirmation(**post)

        order = request.env['sale.order'].sudo().browse(
            request.session.get('sale_last_order_id'))

        # Mark SO as sent
        order.write({'state': 'sent'})

        request.website.sale_reset()
        return request.render("website_sale.confirmation", {'order': order})
