from odoo import models
import logging

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        create_user = False
        allow_create = False
        for line in self.order_line:
            category = line.product_id.categ_id
            while category and not create_user:
                if category.allow_create_user:
                    create_user = True
                category = category.parent_id

        create_user_only_ecommerce = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "website_sale_create_user.create_user_only_ecommerce", default="True"
            )
        )

        create_user_only_ecommerce = create_user_only_ecommerce.lower() in [
            "true",
            "1",
            "t",
            "y",
            "yes",
        ]

        if create_user_only_ecommerce:
            if self.team_id == self.website_id.salesteam_id:
                allow_create = True
        else:
            allow_create = True

        if create_user and allow_create:
            self._create_user_from_order(self.partner_id)
        return res

    def _create_user_from_order(self, partner):
        """Luo käyttäjä tilauksesta annetun partnerin perusteella."""
        existing_user = (
            self.env["res.users"]
            .sudo()
            .search([("login", "=", partner.email)], limit=1)
        )
        logging.info("===KAYTTAJA====");
        logging.info(existing_user);
        logging.info(partner.email);
        if not existing_user:
            # Create a new portal wizard for granting access
            portal_wizard = (
                self.env["portal.wizard"]
                .sudo()
                .create(
                    {
                        "partner_ids": [partner.id],  # Use the partner ID directly
                        "sale_order_id": self.id,
                    }
                )
            )

            # Get wizard user details for the portal access
            portal_user = (
                self.env["portal.wizard.user"]
                .sudo()
                .create(
                    {
                        "wizard_id": portal_wizard.id,
                        "partner_id": partner.id,
                        "email": partner.email,
                    }
                )
            )

            # Grant portal access and send the invitation email
            portal_user.action_grant_access()
