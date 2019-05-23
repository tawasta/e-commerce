# -*- coding: utf-8 -*-
from odoo import fields, models


class WebsiteSaleCouponLog(models.Model):
    
    # 1. Private attributes
    _name = 'website.sale.coupon.log'

    # 2. Fields declaration
    active = fields.Boolean(
        default=True,
    )
    coupon_id = fields.Many2one(
        comodel_name='website.sale.coupon',
        string='Coupon',
        required=True,
    )

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale order',
    )

    sale_order_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string='Order line',
    )

    # 3. Default methods

    # 4. Compute and search fields

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
