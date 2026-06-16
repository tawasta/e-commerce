from odoo import fields, models


class SaleOrderCancellationDenyRule(models.Model):
    _name = "sale.order.cancellation.deny.rule"
    _description = "Sale Order Cancellation Deny Rule"
    _order = "sequence, id"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    domain = fields.Char(
        string="Deny Condition",
        required=True,
        default="[]",
        help="Domain evaluated against sale.order. If it matches, portal cancellation is denied.",
    )