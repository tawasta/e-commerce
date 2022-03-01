from odoo.http import request
from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    @http.route()
    def payment_confirmation(self, **post):
        sale_order_id = request.session.get('sale_last_order_id')
        membership_user = False
        if sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            for line in order.order_line:
                if line.product_id.membership:
                    membership_user = True
            values = {
                "name": order.partner_id.name,
                "partner_id": order.partner_id.id,
                "login": order.partner_id.email,
            }
            partner_user = (
                order.partner_id.user_ids
                and order.partner_id.user_ids[0]
                or False
            )

            if not partner_user:
                new_user = request.env["res.users"].sudo()._signup_create_user(values)
                if new_user:
                    new_user.with_context(create_user=True).action_reset_password()
                    if membership_user:
                        group = request.env["res.groups"].sudo().search([
                            ('membership_group', '=', True)
                        ])

                        if group:
                            group.sudo().write({"users": [(4, new_user.id)]})

        return super(WebsiteSale, self).payment_confirmation(**post)
