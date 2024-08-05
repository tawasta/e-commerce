from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    requires_company_info = fields.Boolean(
        "Requires company info", help="Requires company info on ecommerce checkout"
    )
