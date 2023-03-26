from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    website_show_code = fields.Boolean(
        string="Show code",
        help="Show product code in website",
    )
