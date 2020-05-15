from odoo import models
from odoo import fields


class ProductAttributeValue(models.Model):

    _inherit = "product.attribute.value"

    country_ids = fields.Many2many(
        comodel_name='res.country',
        string='Allowed countries',
        help='Allow for these countries. Leave empty to allow for all.',
    )
