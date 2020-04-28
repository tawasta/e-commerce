from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    website_synopsis = fields.Char(
        string="Website synopsis",
        help="Show product synopsis in website",
    )
