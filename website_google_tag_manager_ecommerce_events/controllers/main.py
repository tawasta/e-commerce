import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class WebsiteSaleGTM(http.Controller):
    @http.route(
        "/shop/ga4/item",
        type="json",
        auth="public",
        website=True,
    )
    def ga4_item(self, product_id, quantity=1.0, **kwargs):
        """Return a GA4 ecommerce payload for a single product, used by
        the add_to_cart frontend patch."""

        product = request.env["product.product"].sudo().browse(int(product_id))
        if not product.exists():
            return {}
        website = request.env["website"].get_current_website()
        ga4_item = {
            "currency": website.currency_id.name,
            "value": product.lst_price * float(quantity),
            "items": [product._ga4_item(quantity=float(quantity))],
        }

        return ga4_item
