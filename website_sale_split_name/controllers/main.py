from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    @http.route()
    def address(self, **kw):
        if 'submitted' in kw:
            name = request.env["res.partner"]._get_computed_name(kw.get("lastname"), kw.get("firstname"))
            kw["name"] = name
            response = super(WebsiteSale, self).address(**kw)
        else:
            response = super(WebsiteSale, self).address(**kw)

        return response
