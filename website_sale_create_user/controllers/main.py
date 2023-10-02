from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    @http.route()
    def payment_confirmation(self, **post):
        sale_order_id = request.session.get("sale_last_order_id")
        membership_user = False
        if sale_order_id:
            order = request.env["sale.order"].sudo().browse(sale_order_id)
            for line in order.order_line:
                if line.product_id.membership:
                    membership_user = True
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
                # Check if this user already exists
                partner_user = res_users.search([("login", "=", values.get("login"))])

            if not partner_user:
                # admin_user = res_users.search([("id", "=", "2")])
                new_user = request.env["res.users"].sudo()._signup_create_user(values)
                if new_user:
                    new_user.with_context(create_user=True).action_reset_password()
                    template = request.env.ref(
                        "auth_signup.set_password_email", raise_if_not_found=False
                    )
                    template_values = {
                        "email_to": new_user.partner_id.email,
                        "email_cc": False,
                        "auto_delete": True,
                        "partner_to": False,
                        "scheduled_date": False,
                    }
                    if membership_user:
                        attachment_ids = (
                            request.env["ir.attachment"]
                            .sudo()
                            .search([("membership_attachment", "=", True)])
                        )
                        template_values.update(
                            {
                                "attachment_ids": [
                                    (4, att.id) for att in attachment_ids
                                ],
                            }
                        )
                        group = (
                            request.env["res.groups"]
                            .sudo()
                            .search([("membership_group", "=", True)])
                        )

                        if group:
                            group.sudo().write({"users": [(4, new_user.id)]})

                    template.sudo().write(template_values)
                    template.sudo().send_mail(
                        new_user.id, force_send=True, raise_exception=True
                    )

        return super(WebsiteSale, self).payment_confirmation(**post)
