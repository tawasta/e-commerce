import logging

from odoo import http
from odoo.http import request

from odoo.addons.auth_signup.models.res_partner import now
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    @http.route()
    def payment_confirmation(self, **post):
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
                    email_template_values = self.handle_new_user(order, new_user)
                    logging.info(email_template_values)
                    if email_template_values:
                        self.send_email(new_user, email_template_values)

        return super(WebsiteSale, self).payment_confirmation(**post)

    def handle_new_user(self, order, new_user):

        # prepare reset password signup
        create_mode = False

        # no time limit for initial invitation, only for reset password
        expiration = False if create_mode else now(days=+1)

        # Signup prepare for the partner linked to the new user
        new_user.partner_id.signup_prepare(signup_type="reset", expiration=expiration)

        template_values = {
            "email_to": new_user.partner_id.email,
            "email_cc": False,
            "auto_delete": True,
            "partner_to": False,
            "scheduled_date": False,
        }
        logging.info(template_values)
        return template_values

    def send_email(self, new_user, template_values):
        template = request.env.ref(
            "auth_signup.set_password_email", raise_if_not_found=False
        )
        if template:
            template.sudo().write(template_values)
            template.sudo().send_mail(
                new_user.id, force_send=True, raise_exception=True
            )
