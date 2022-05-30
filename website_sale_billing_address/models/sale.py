from odoo import models, api, fields
from odoo.tools.translate import _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    use_different_billing_address = fields.Boolean(default=False)
