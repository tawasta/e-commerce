from odoo import fields, models


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    price_with_tax = fields.Float(
        string="Price with tax", compute="_compute_price_with_tax",
    )

    def _compute_price_with_tax(self):
        for record in self:
            price = record.fixed_price
            tax_amount = 0
            for tax in record.product_id.taxes_id:
                tax_ids = tax.compute_all(price, record.currency_id).get("taxes")

                if tax_ids:
                    tax_amount += tax_ids[0]["amount"]

            record.price_with_tax = price + tax_amount
