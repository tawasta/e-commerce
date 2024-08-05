from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    requires_explanation = fields.Boolean("Requires an explanation")
    requires_explanation_help = fields.Text(
        "Explanation text",
        help="Show this help text if explanation is missing for this product",
    )
