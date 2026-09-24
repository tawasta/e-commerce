from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    @http.route()
    def address(self, **kw):
        response = super().address(**kw)

        order = request.website.sale_get_order()

        if "submitted" in kw and kw.get("year_of_birth"):
            order.partner_id.sudo().write({"year_of_birth": kw.get("year_of_birth")})

        # /shop/address redirects instead of rendering once the address is
        # saved, and a redirect response has no qcontext to extend.
        if hasattr(response, "qcontext"):
            response.qcontext["has_membership_product"] = self._has_membership_product(
                order
            )
            response.qcontext["current_year_of_birth"] = order.partner_id.year_of_birth

        return response

    def _has_membership_product(self, order):
        if not order:
            return False
        return any(line.product_id.membership for line in order.order_line)
