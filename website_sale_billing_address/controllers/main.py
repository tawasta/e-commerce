from odoo import http
from odoo.http import request
import logging
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleBilling(WebsiteSale):
    @http.route()
    def address(self, **kw):
        new_billing = False
        order = request.website.sale_get_order()
        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            new_billing = True
        response = super(WebsiteSaleBilling, self).address(**kw)
        order = request.website.sale_get_order()
        if "submitted" in kw:
            if not kw.get("billing_use_same") and new_billing:
                order.sudo().write({"use_different_billing_address": True})
                return request.redirect("/shop/address?mode=billing")
            else:
                if kw.get("is_billing_mode") and kw.get("vat"):
                    order.partner_invoice_id.sudo().write(
                        {"company_registry": kw.get("vat")}
                    )
                return response
        else:
            return response
