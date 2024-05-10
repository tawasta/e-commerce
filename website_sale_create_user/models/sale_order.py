from odoo import models


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
            self._create_user_from_order()
        return res

    def _create_user_from_order(self):

        existing_user = (
            self.env["res.users"]
            .sudo()
            .search([("login", "=", self.partner_id.email)], limit=1)
        )
        if not existing_user:
            user_values = {
                "partner_id": self.partner_id.id,
                "email": self.partner_id.email,
                "in_portal": True,
            }

            wizard = (
                self.env["portal.wizard"]
                .sudo()
                .create({"user_ids": [(0, 0, user_values)], "sale_order_id": self.id})
            )
            wizard.action_apply()
