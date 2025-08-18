from odoo import http
from odoo.http import request
import logging
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)

class MyWebsiteSale(WebsiteSale):

    @http.route()
    def shop_payment(self, **post):
        if not request.session.get('checkout_done'):
            return request.redirect('/shop/checkout')
        return super().shop_payment(**post)

    @http.route()
    def checkout(self, **post):
        response = super().checkout(**post)
        if not post:
            request.session['checkout_done'] = True
        return response


    @http.route()
    def confirm_order(self, **post):
        if not request.session.get('checkout_done'):
            return request.redirect('/shop/checkout')
        return super().confirm_order(**post)


    @http.route()
    def shop_payment_confirmation(self, **post):
        response = super().shop_payment_confirmation(**post)

        # Kun maksu vahvistettu, poistetaan checkout_done
        if request.session.get('checkout_done'):
            request.session.pop('checkout_done', None)

        return response

