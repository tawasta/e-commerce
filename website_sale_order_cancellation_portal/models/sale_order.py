from datetime import timedelta

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    portal_cancellation_ids = fields.One2many(
        "sale.order.cancellation",
        "sale_order_id",
        string="Cancellation Notices",
        copy=False,
    )

    portal_cancellation_received = fields.Boolean(
        string="Cancellation Notice Received",
        copy=False,
        readonly=True,
    )

    portal_cancellation_deadline = fields.Datetime(
        string="Cancellation Deadline",
        compute="_compute_portal_cancellation_deadline",
    )

    portal_cancellation_allowed = fields.Boolean(
        compute="_compute_portal_cancellation_allowed",
    )

    def _get_portal_cancellation_period_days(self):
        value = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "website_sale_order_cancellation_portal.period_days",
                "14",
            )
        )
        try:
            value = int(value)
        except Exception:
            value = 14
        return max(value, 0)

    def _compute_portal_cancellation_deadline(self):
        for order in self:
            if not order.date_order:
                order.portal_cancellation_deadline = False
                continue

            order.portal_cancellation_deadline = order.date_order + timedelta(
                days=order._get_portal_cancellation_period_days()
            )

    def _has_portal_cancellable_lines(self):
        self.ensure_one()
        return bool(
            self.order_line.filtered(
                lambda line: not line.display_type and line.product_uom_qty > 0
            )
        )

    def _compute_portal_cancellation_allowed(self):
        now = fields.Datetime.now()

        for order in self:
            order.portal_cancellation_allowed = bool(
                order.state != "cancel"
                and not order.portal_cancellation_received
                and not order.portal_cancellation_ids
                and order.portal_cancellation_deadline
                and order.portal_cancellation_deadline >= now
                and order._has_portal_cancellable_lines()
            )
