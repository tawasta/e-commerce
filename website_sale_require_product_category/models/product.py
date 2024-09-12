from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    required_product_category_id = fields.Many2one(
        string="Required product category", comodel_name="product.public.category"
    )
    required_product_category_help = fields.Text(
        "Required category help",
        translate=True,
        help="Show this help text if a product from required category is missing from order",
    )
