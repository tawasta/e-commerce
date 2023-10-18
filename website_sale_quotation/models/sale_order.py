from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    amount_total = fields.Monetary(groups="base.group_user")
