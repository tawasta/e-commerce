from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    requires_explanation = fields.Boolean("Requires an explanation")
    requires_explanation_help = fields.Text(
        "Explanation help",
        translate=True,
        help="Show this help text if order explanation is missing",
    )
