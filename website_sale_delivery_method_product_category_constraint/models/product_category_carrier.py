from odoo import api
from odoo import fields
from odoo import models


class ProductCategoryCarrier(models.Model):

    _name = 'product.category.carrier'
    _rec_name = 'carrier'

    name = fields.Char(string="Name")

    product_category = fields.Many2one(
        comodel_name='product.category', string='Product Category')

    carrier = fields.Many2one(
        comodel_name='delivery.carrier', string='Delivery method', required=True)

    @api.model
    def create(self, values):
        """Assign the next sequence"""
        values["name"] = self.env["ir.sequence"].next_by_code(
            "product.category.carrier")
        return super(ProductCategoryCarrier, self).create(values)
