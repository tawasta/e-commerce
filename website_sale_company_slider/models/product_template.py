from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    hide_company_slider = fields.Boolean(
        "Hide company slider",
        help="Hide company slider from e-commerce checkout, if this product is present",
    )
