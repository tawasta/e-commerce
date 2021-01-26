from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleContact(WebsiteSale):
    @http.route()
    def address(self, **kw):
        res = super().address(**kw)

        order = request.website.sale_get_order()

        if order.partner_id.company_name or order.partner_id.parent_id:
            if not order.customer_contact_id:
                order.customer_contact_id = order.partner_id.id

        return res
