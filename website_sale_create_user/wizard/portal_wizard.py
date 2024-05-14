import logging

from odoo import _, fields, models
from odoo.exceptions import UserError


class PortalWizard(models.TransientModel):
    _inherit = "portal.wizard"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order")


class PortalWizardUser(models.TransientModel):
    _inherit = "portal.wizard.user"

    def _send_email(self):
        # if not self.env.user.email:
        #     raise UserError(
        #         _(
        #             "You must have an email address in your User Preferences to send emails."
        #         )
        #     )

        template = self.env.ref("portal.mail_template_data_portal_welcome")

        for wizard_line in self:
            lang = wizard_line.user_id.lang
            partner = wizard_line.user_id.partner_id
            portal_url = partner.with_context(
                signup_force_type_in_url="", lang=lang
            )._get_signup_url_for_action()[partner.id]
            partner.signup_prepare()

            context = {
                "dbname": self._cr.dbname,
                "portal_url": portal_url,
                "lang": lang,
            }

            attachment_ids = []
            if wizard_line.wizard_id.sale_order_id:
                product_categories = (
                    wizard_line.wizard_id.sale_order_id.order_line.mapped(
                        "product_id.categ_id"
                    )
                )
                while product_categories:
                    for category in product_categories:
                        if (
                            category.create_user_attachment
                            and category.allow_create_user
                        ):
                            attachment_ids.append(category.create_user_attachment.id)
                    # Move up in the category hierarchy
                    product_categories = product_categories.mapped("parent_id")

            if attachment_ids:
                email_values = {"attachment_ids": [(6, 0, attachment_ids)]}
            else:
                email_values = {}

            if template:
                template.with_context(**context).send_mail(
                    wizard_line.id, force_send=True, email_values=email_values
                )
            else:
                logging.warning(
                    "No email template found for sending email to the portal user"
                )

        return True
