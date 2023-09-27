from odoo import http
import logging
from odoo.http import request
from odoo.addons.payment.controllers.portal import PaymentProcessing

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleForceAddress(WebsiteSale):
    @http.route()
    def payment(self, **post):
        order = request.website.sale_get_order()

        if order:
            order.action_quotation_sent()
            request.website.sale_reset()

        return request.redirect('/shop/confirmation')
