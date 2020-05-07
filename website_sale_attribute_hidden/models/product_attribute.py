from odoo import models
from odoo import fields


class ProductAttribute(models.Model):

    _inherit = "product.attribute"

    website_published = fields.Boolean(
        string="Website published",
        default=True,
    )
