from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _should_show_quantity_selector(self):
        """Check if the product's category has disabled quantity changes."""
        self.ensure_one()
        return not self.product_id.categ_id.disable_qty_change
