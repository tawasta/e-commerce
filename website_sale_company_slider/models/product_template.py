from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    hide_company_slider = fields.Boolean(
        "Hide company slider",
        help="Hide company slider from e-commerce checkout, if this product is present",
    )

    force_company_slider = fields.Boolean(
        "Force company slider",
        help="Force company for company slider in e-commerce checkout, if this product is present",
    )
