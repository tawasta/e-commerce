from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    inventory_availability = fields.Selection(
        selection_add=[
            (
                "delivery_time",
                "Show the stock balance in the online store, if the product is not in stock, show the delivery time",
            )
        ]
    )
