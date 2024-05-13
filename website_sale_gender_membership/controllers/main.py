from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSale(WebsiteSale):
    @http.route()
    def address(self, **kw):
        response = super(WebsiteSale, self).address(**kw)
        order = request.website.sale_get_order()
        
        has_membership_product = any(
            line.product_id.membership for line in order.order_line if line.product_id.membership
        )
        
        if "submitted" in kw:
            if kw.get("gender"):
                order.partner_id.sudo().write({"gender": kw.get("gender")})
                
        # Lisätään has_membership_product kontekstiin
        response.qcontext['has_membership_product'] = has_membership_product
        return response
