from odoo import fields
from odoo import models


class ProductCategory(models.Model):

    _inherit = 'product.category'

    category_carrier = fields.One2many(comodel_name='product.category.carrier',
                                       inverse_name='product_category',
                                       string="Product Category carrier")
