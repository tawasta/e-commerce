from odoo import SUPERUSER_ID, http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleUser(WebsiteSale):
    @http.route()
    def payment_confirmation(self, **post):
        sale_order_id = request.session.get("sale_last_order_id")
        if sale_order_id:
            order = request.env["sale.order"].sudo().browse(sale_order_id)
            partner = order.partner_id
            user_values = {
                "partner_id": partner.id,
                "email": partner.email,
                "in_portal": True,
            }
            wizard_values = {"user_ids": [(0, 0, user_values)]}
            portal_wizard = request.env["portal.wizard"].sudo().create(wizard_values)
            portal_wizard.sudo().with_user(SUPERUSER_ID).action_apply()

        return super(WebsiteSaleUser, self).payment_confirmation(**post)
