from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.public.category"

    suggested_products_category_id = fields.Many2one(
        comodel_name="suggested.products.category",
        string="Suggested Accessory Products Category",
        help="In cart, in which Suggested Accessory Product Category should this "
        "category's products be combined under.",
    )
