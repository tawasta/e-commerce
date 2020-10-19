from odoo import fields
from odoo import models


class ProductCategory(models.Model):

    _inherit = 'product.category'

    category_carrier = fields.Many2many(
        comodel_name='delivery.carrier',
        string="Allowed Delivery methods")
