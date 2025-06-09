from odoo import models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        for order in self:
            # Tarkista, onko laskutustuote jo lisätty
            tx = order.transaction_ids and order.transaction_ids[0]
            product = tx.payment_method_id.product_id if tx else None
            if product:
                already_added = any(
                    line.product_id.id == product.id for line in order.order_line
                )
                if not already_added:
                    desc = (
                        f"[{product.default_code}] {product.name}"
                        if product.default_code
                        else product.name
                    )
                    self.env["sale.order.line"].sudo().create(
                        {
                            "order_id": order.id,
                            "product_id": product.id,
                            "product_uom_qty": 1,
                            "price_unit": product.list_price,
                            "name": desc,
                            "company_id": order.company_id.id,
                            "customer_lead": 0,
                        }
                    )
        return super(SaleOrder, self).action_confirm()
