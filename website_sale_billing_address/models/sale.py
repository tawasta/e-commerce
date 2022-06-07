from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    use_different_billing_address = fields.Boolean(default=False)
