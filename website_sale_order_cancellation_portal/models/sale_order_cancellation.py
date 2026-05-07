from odoo import fields, models


class SaleOrderCancellation(models.Model):
    _name = "sale.order.cancellation"
    _description = "Sale Order Cancellation Notice"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "received_at desc"
    _rec_name = "sale_order_id"

    sale_order_id = fields.Many2one(
        "sale.order",
        string="Sale Order",
        required=True,
        ondelete="cascade",
        tracking=True,
    )

    partner_id = fields.Many2one(
        related="sale_order_id.partner_id",
        string="Customer",
        store=True,
        readonly=True,
    )

    received_at = fields.Datetime(
        string="Received At",
        default=fields.Datetime.now,
        required=True,
        readonly=True,
        tracking=True,
    )

    cancellation_reason = fields.Text(
        string="Cancellation Reason",
        help="Optional reason given by the customer.",
    )