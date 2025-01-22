from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    disable_qty_change = fields.Boolean(
        string="Disable Quantity Change",
        help="If enabled, quantity change in the cart will be disabled for products in this category."
    )
