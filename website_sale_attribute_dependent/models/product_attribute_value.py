from odoo import api
from odoo import models
from odoo import fields
from odoo import _
from odoo.exceptions import ValidationError


class ProductAttributeValue(models.Model):

    _inherit = "product.attribute.value"

    dependent_attribute_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        relation='product_dependent_attribute_ids_rel',
        column1='src_id',
        column2='dest_id',
        string='Dependent attributes',
        help='Attribute values to be suggested by default, '
             'when this attribute value is selected'
    )

    @api.constrains('dependent_attribute_ids')
    def _check_something(self):
        # Try to disallow doing impossible or recursive dependencies
        for record in self:
            for attribute in record.dependent_attribute_ids:
                # Don't allow depending on the current attribute
                if record.attribute_id == attribute.attribute_id:
                    raise ValidationError(
                        _("Dependent value must be from a different attribute")
                    )

            dependent_count = len(record.dependent_attribute_ids)
            attributes_count = len(
                record.dependent_attribute_ids.mapped('attribute_id'))

            # Don't allow using values with same attribute more than once
            if dependent_count > attributes_count:
                raise ValidationError(
                    _("Each attribute can be used only once")
                )
