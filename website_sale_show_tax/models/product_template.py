# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    website_tax_ids = fields.Many2many(
        comodel_name='account.tax',
        help='Taxes that are applied to website price',
        compute='_compute_website_tax_ids',
    )

    def _compute_website_tax_ids(self):
        # First filter out the ones that have no variant:
        # This makes sure that every template below has a corresponding product
        # in the zipped result.
        self = self.filtered('product_variant_id')
        # Use mapped that returns a recordset with only itself to prefetch
        # and don't prefetch every product_variant_ids
        for template, product in zip(self, self.mapped('product_variant_id')):
            template.website_tax_ids = product.website_tax_ids
