from odoo import models
from odoo import fields


class ProductAttributeValue(models.Model):

    _inherit = "product.attribute.value"

    dependency_id = fields.Many2one(
        comodel_name='product.attribute.value',
        string='Dependent for',
    )

    dependent_attribute_ids = fields.One2many(
        comodel_name='product.attribute.value',
        inverse_name='dependency_id',
        string='Dependent attributes',
        help='Attribute values to be suggested by default, '
             'when this attribute value is selected'
    )
