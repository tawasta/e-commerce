# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models, _

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    coupon_log_ids = fields.One2many(
        comodel_name='website.sale.coupon.log',
        inverse_name='sale_order_line_id',
        string='Coupon log',
    )

    is_coupon = fields.Boolean(
        string='Is a coupon',
        compute=lambda self: self._compute_is_coupon(),
    )

    def _use_coupon(self, coupon):
        # Use the coupon if it's appicable to this SO line
        # Returns True if the code is used
        # Returns False if the code can't be used

        # Skip checks on coupon lines
        if self.is_coupon:
            return False

        # Check if the coupon has a product limitation
        if coupon.product_id and coupon.product_id != self.product_id:
            return False

        # Check if the coupon has a product group limitation
        if coupon.category_id and coupon.category_id != self.product_id.categ_id:
            return False

        # Don't allow using same fixed discounts twice
        coupon_used = self.env['website.sale.coupon.log'].search([
            ('coupon_id', '=', coupon.id),
            ('sale_order_id', '=', self.order_id.id),
            ('coupon_id.type', '=', 'fixed'),
        ], limit=1)

        if coupon_used:
            return False

        # Don't allow using two percent discounts for line (Not implemented)
        if coupon.type == 'percent':
            coupon_used = self.env['website.sale.coupon.log'].search([
                ('coupon_id.type', '=', 'percent'),
                ('sale_order_line_id', '=', self.id),
            ], limit=1)

        if coupon_used:
            return False

        # Everything is fine. Create a new coupon log entry
        coupon_log_vals = {
            'coupon_id': coupon.id,
            'sale_order_id': self.order_id.id,
            'sale_order_line_id': self.id,
        }

        self.coupon_log_ids = [(0, 0, coupon_log_vals)]

        self._add_coupon(coupon)

        # Tell the method caller that the coupon was used
        return True

    @api.multi
    def _add_coupon(self, coupon):
        # Add coupon as new SO line or as line discount
        discount_product = self.env.ref('website_sale_coupon.product_product_coupon')
        coupon_log_model = self.env['website.sale.coupon.log']

        for record in self:
            if record.is_coupon:
                # Skip coupon product lines
                continue

            if coupon.type == 'fixed':
                # Add a negative line
                description = _('Discount code %s (%s)' % (coupon.name, coupon.code))

                used_coupon = coupon_log_model.search([
                    ('coupon_id', '=', coupon.id),
                    ('sale_order_line_id', '=', record.id),
                ])

                order_line = {
                    'product_id': discount_product.id,
                    'description': description,
                    'order_id': record.order_id.id,
                    'price_unit': -1 * coupon.value,
                    'coupon_log_ids': [(6, 0, [used_coupon.id])],
                }
                record.env['sale.order.line'].create(order_line)

            elif coupon.type == 'percent':
                # Add a discount
                record.discount = coupon.value

    @api.multi
    def _compute_is_coupon(self):
        # Helper for deciding if SO line is for a coupon product
        discount_product = self.env.ref('website_sale_coupon.product_product_coupon')
        for record in self:
            record.is_coupon = record.product_id == discount_product
