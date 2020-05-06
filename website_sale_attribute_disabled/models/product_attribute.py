from odoo import models
from odoo import fields


class ProductAttribute(models.Model):

    _inherit = "product.attribute"

    website_disabled = fields.Boolean(
        string="Website disabled",
    )
