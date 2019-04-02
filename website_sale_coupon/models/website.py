# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models, _
from odoo.http import request

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class Website(models.Model):

    _inherit = 'website'

    @api.multi
    def sale_get_order(self, force_create=False, code=None, update_pricelist=False, force_pricelist=False):
        # Store voucher price_units and update them.
        # We don't want to use the actual price '0' here.
        # We also don't want to create separate product variants for each coupon line

        self.ensure_one()
        partner = self.env.user.partner_id
        sale_order_id = request.session.get('sale_order_id')
        if not sale_order_id:
            last_order = partner.last_website_so_id
            available_pricelists = self.get_pricelist_available()

            sale_order_id = last_order.state == 'draft' and \
                            last_order.pricelist_id in available_pricelists and \
                            last_order.id

        sale_order = self.env['sale.order'].sudo().browse(sale_order_id).exists() if sale_order_id else None

        if sale_order:
            # Store the prices
            coupon_lines = dict()
            for order_line in sale_order.order_line:
                if order_line.is_coupon:
                    coupon_lines[order_line.id] = order_line.price_unit

        res = super(Website, self).sale_get_order(
            force_create=force_create,
            code=code,
            update_pricelist=update_pricelist,
            force_pricelist=force_pricelist
        )

        if sale_order:
            # Re-add the prices
            for order_line in sale_order.order_line:
                if order_line.id in coupon_lines:
                    order_line.price_unit = coupon_lines[order_line.id]

        return res