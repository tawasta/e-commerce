from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    website_variant_header = fields.Char(
        string="Website variant header",
        help="Show product variant header in website",
    )
