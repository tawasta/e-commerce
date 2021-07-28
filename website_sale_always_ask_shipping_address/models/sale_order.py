from odoo import api
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    @api.depends("website_order_line.product_uom_qty", "website_order_line.product_id")
    def _compute_cart_info(self):
        super()._compute_cart_info()

        for order in self:
            # Override the "only services" to be always false
            # This will cause the shipping address to be always asked
            order.only_services = False
