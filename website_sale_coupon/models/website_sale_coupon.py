# -*- coding: utf-8 -*-

# 1. Standard library imports:
import random
import string

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models, _

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class WebsiteSaleCoupon(models.Model):
    
    # 1. Private attributes
    _name = 'website.sale.coupon'

    # 2. Fields declaration
    name = fields.Char(
        string='Name',
        required=True,
        help='Used on sale order and invoice',
    )
    code = fields.Char(
        string='Code',
        default=lambda self: self._compute_default_code(),
        required=True,
        help='Give this to your customer(s)',
    )
    active = fields.Boolean(
        default=True,
    )
    description = fields.Char(
        string='Description',
        help='For internal use only. This will not be shown to the customer',
    )
    # Allowed product
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        help='Allowed product. Leave empty if applies to any product',
    )
    # Allowed category
    category_id = fields.Many2one(
        comodel_name='product.category',
        string='Product category',
        help='Allowed category. Leave empty if applies to any category',
    )
    # Allowed partner
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        help='Allowed partner. Leave empty if applies to any partner',
    )
    start_date = fields.Datetime(
        string='Valid from',
    )
    end_date = fields.Datetime(
        string='Valid to'
    )
    available = fields.Integer(
        string='Available usages',
        help='0 = not available. -1 = infinite available',
        default=1,
    )
    value = fields.Float(
        string='Coupon value',
        help='Discount amount. For percentage, 50.0 means "50%" and 0.50 means "0.50%".'
    )
    type = fields.Selection(
        string='Coupon type',
        selection=[
            ('fixed', 'Fixed'),
            ('percent', 'Percentage'),
        ],
        default='fixed',
    )
    log_ids = fields.One2many(
        comodel_name='website.sale.coupon.log',
        inverse_name='coupon_id',
        string='Coupon usage',
    )

    # 3. Default methods
    def _compute_default_code(self):
        # Generate a pseudo-random coupon code
        coupon_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

        return coupon_code

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges
    _sql_constraints = [
        ('name_unique', 'unique (code)', 'This code already exists!'),
    ]

    # 6. CRUD methods
    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}

        if not default.get('name'):
            default['name'] = _("%s (copy)") % self.name

        default['code'] = self._compute_default_code()

        return super(WebsiteSaleCoupon, self).copy(default)

    # 7. Action methods

    # 8. Business methods
