from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    @http.route()
    def address(self, **kw):
        if "submitted" in kw:
            response = super(WebsiteSale, self).address(**kw)
            if kw.get("birth_year"):
                order = request.website.sale_get_order()
                birth_year = (
                    request.env["res.birth.year"]
                    .sudo()
                    .search([("id", "=", kw.get("birth_year"))])
                )
                order.partner_id.sudo().write({"birth_year": birth_year.id})
        else:
            response = super(WebsiteSale, self).address(**kw)

        return response
