from odoo import models

from .product_product import _ga4_push_script


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _ga4_items(self):
        """Return GA4 `items` array from order lines, skipping delivery
        lines and lines without a product (sections, notes)."""
        self.ensure_one()
        items = []
        for line in self.order_line:
            if not line.product_id:
                continue
            if line.is_delivery:
                continue
            items.append(
                line.product_id._ga4_item(
                    quantity=line.product_uom_qty,
                    price=line.price_unit,
                )
            )
        return items

    def _ga4_begin_checkout_script(self):
        self.ensure_one()
        payload = {
            "event": "begin_checkout",
            "ecommerce": {
                "currency": self.currency_id.name,
                "value": self.amount_untaxed,
                "items": self._ga4_items(),
            },
        }
        return _ga4_push_script(payload)

    def _ga4_purchase_script(self):
        self.ensure_one()
        shipping = sum(line.price_total for line in self.order_line if line.is_delivery)
        payload = {
            "event": "purchase",
            "ecommerce": {
                "transaction_id": self.name,
                "currency": self.currency_id.name,
                "value": self.amount_total,
                "tax": self.amount_tax,
                "shipping": shipping,
                "items": self._ga4_items(),
            },
        }
        return _ga4_push_script(payload)
