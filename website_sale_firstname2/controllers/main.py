from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    @http.route()
    def address(self, **kw):
        if "submitted" in kw:
            response = super(WebsiteSale, self).address(**kw)
            if kw.get("firstname2"):
                order = request.website.sale_get_order()
                order.partner_id.sudo().write({"firstname2": kw.get("firstname2")})
        else:
            response = super(WebsiteSale, self).address(**kw)

        return response
