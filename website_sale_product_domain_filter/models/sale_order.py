from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _cart_accessories(self):
        accessories = super()._cart_accessories()

        accessories = self.env["product.product"].browse([p.id for p in accessories])

        accessories = accessories.filtered(
            lambda p: p.product_tmpl_id.user_in_partner_domain
        )

        return accessories
