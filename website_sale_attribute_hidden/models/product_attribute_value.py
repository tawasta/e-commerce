from odoo import models
from odoo import fields


class ProductAttributeValue(models.Model):

    _inherit = "product.attribute.value"

    website_published = fields.Boolean(
        string="Website published",
        default=True,
    )
