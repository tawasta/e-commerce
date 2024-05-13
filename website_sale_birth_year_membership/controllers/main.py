from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSale(WebsiteSale):
    @http.route()
    def address(self, **kw):
        response = super(WebsiteSale, self).address(**kw)
        
        order = request.website.sale_get_order()
        has_membership = self._has_membership_product(order)
        response.qcontext['has_membership_product'] = has_membership

        if "submitted" in kw:
            if kw.get("year_of_birth"):
                order.partner_id.sudo().write({"year_of_birth": kw.get("year_of_birth")})

        return response

    def _has_membership_product(self, order):
        if order:
            return any(line.product_id.membership for line in order.order_line)
        return False
