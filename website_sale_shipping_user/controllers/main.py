from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request


class WebsiteSale(WebsiteSale):
    @http.route()
    def payment_confirmation(self, **post):
        res = super().payment_confirmation(**post)
        sale_order_id = request.session.get("sale_last_order_id")
        order = False

        if sale_order_id:
            order = request.env["sale.order"].sudo().browse(sale_order_id)

        if order and order.partner_id != order.partner_shipping_id:
            # Create user for shipping address
            shipping = order.partner_shipping_id
            company_id = order.company_id.id
            user_values = {
                "email": shipping.email,
                "login": shipping.email,
                "partner_id": shipping.id,
                "company_id": company_id,
                "company_ids": [(6, 0, [company_id])],
            }
            user = (
                request.env["res.users"]
                .with_context(no_reset_password=True)
                .sudo()
                .with_delay()
                ._delayed_create_user_from_template(user_values)
            )

            # Set new user as SO follower
            order.message_partner_ids += user.partner_id

            # Send an invitation email
            user.with_context(create_user=True).action_reset_password()

        return res
