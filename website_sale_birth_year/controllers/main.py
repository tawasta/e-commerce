from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    @http.route()
    def address(self, **kw):
        if "submitted" in kw:
            response = super(WebsiteSale, self).address(**kw)

            # Store year of birth to partner
            if kw.get("year_of_birth"):
                order = request.website.sale_get_order()
                order.partner_id.sudo().write(
                    {"year_of_birth": kw.get("year_of_birth")}
                )
        else:
            response = super(WebsiteSale, self).address(**kw)

        return response
