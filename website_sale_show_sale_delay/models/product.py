from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    inventory_availability = fields.Selection(
        selection_add=[
            (
                "delivery_time",
                "When the stock balance is below the limit, show the delivery time",
            )
        ]
    )
