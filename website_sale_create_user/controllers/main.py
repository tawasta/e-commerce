from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    @http.route()
    def shop_payment_confirmation(self, **post):
        sale_order_id = request.session.get("sale_last_order_id")
        if sale_order_id:
            order = request.env["sale.order"].sudo().browse(sale_order_id)
            values = {
                "name": order.partner_id.name,
                "partner_id": order.partner_id.id,
                "login": order.partner_id.email,
            }
            partner_user = (
                order.partner_id.user_ids and order.partner_id.user_ids[0] or False
            )
            res_users = request.env["res.users"].sudo()

            if not partner_user:
                partner_user = res_users.search([("login", "=", values.get("login"))])

            if not partner_user:
                new_user = request.env["res.users"].sudo()._signup_create_user(values)
                if new_user:
                    website = request.env["website"].get_current_website()
                    new_user.sudo().write(
                        {
                            "company_id": website.company_id.id,
                            "company_ids": [(6, 0, website.company_id.ids)],
                        }
                    )
                    new_user.with_context(create_user=True).action_reset_password()
                    self.handle_new_user(order, new_user)

        return super(WebsiteSale, self).shop_payment_confirmation(**post)

    def handle_new_user(self, order, new_user):
        # Tässä metodissa toteutetaan perustoiminnot uudelle käyttäjälle.
        # Tämä metodi voidaan korvata toisessa moduulissa.
        pass
