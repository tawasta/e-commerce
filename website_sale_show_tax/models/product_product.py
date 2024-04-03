
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    website_tax_ids = fields.Many2many(
        comodel_name='account.tax',
        help='Taxes that are applied to website price',
        compute='_compute_website_tax_ids',
    )

    def _compute_website_tax_ids(self):
        current_website = self.env['website'].get_current_website()
        partner = self.env.user.partner_id
        company_id = current_website.company_id

        for product in self:
            # Get taxes depending on partner fiscal position
            tax_ids = partner.property_account_position_id.sudo().map_tax(
                product.taxes_id.sudo().filtered(
                    lambda x: x.company_id == company_id)
            )

            product.website_tax_ids = tax_ids
