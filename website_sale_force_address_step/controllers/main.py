from odoo import http
from odoo.http import request
import logging
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class MyWebsiteSale(WebsiteSale):

    @http.route()
    def shop_payment(self, **post):
        _logger.info("==> shop_payment CALLED | checkout_done=%s | post=%s", request.session.get("checkout_done"), post)
        if not request.session.get("checkout_done"):
            _logger.info("Redirecting to /shop/checkout (checkout_done missing)")
            return request.redirect("/shop/checkout")

        _logger.info("Proceeding with super().shop_payment()")
        return super().shop_payment(**post)

    @http.route()
    def checkout(self, **post):
        _logger.info("==> checkout CALLED | post=%s", post)
        response = super().checkout(**post)

        if not post:
            request.session["checkout_done"] = True
            _logger.info("checkout_done FLAG SET to True (post empty)")
        else:
            _logger.info("checkout_done FLAG NOT SET (post had data)")

        return response

    @http.route()
    def confirm_order(self, **post):
        _logger.info("==> confirm_order CALLED | checkout_done=%s | post=%s", request.session.get("checkout_done"), post)
        if not request.session.get("checkout_done"):
            _logger.info("Redirecting to /shop/checkout (checkout_done missing)")
            return request.redirect("/shop/checkout")

        _logger.info("Proceeding with super().confirm_order()")
        return super().confirm_order(**post)

    @http.route()
    def shop_payment_confirmation(self, **post):
        _logger.info("==> shop_payment_confirmation CALLED | checkout_done=%s | post=%s", request.session.get("checkout_done"), post)
        response = super().shop_payment_confirmation(**post)

        if request.session.get("checkout_done"):
            _logger.info("checkout_done FLAG REMOVED after payment confirmation")
            request.session.pop("checkout_done", None)
        else:
            _logger.info("checkout_done FLAG already missing (no removal needed)")

        return response
