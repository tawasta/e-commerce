from datetime import timedelta

from odoo import fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


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

    portal_cancellation_denial_rule_id = fields.Many2one(
        "sale.order.cancellation.deny.rule",
        string="Cancellation Denial Rule",
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
            order.portal_cancellation_deadline = (
                order.date_order
                and order.date_order
                + timedelta(days=order._get_portal_cancellation_period_days())
            )

    def _has_portal_cancellable_lines(self):
        self.ensure_one()
        return bool(
            self.order_line.filtered(
                lambda line: not line.display_type and line.product_uom_qty > 0
            )
        )

    def _get_portal_cancellation_denial_rule(self):
        self.ensure_one()

        rules = self.env["sale.order.cancellation.deny.rule"].sudo().search([
            ("active", "=", True),
        ])

        for rule in rules:
            try:
                rule_domain = safe_eval(rule.domain or "[]")
            except Exception:
                continue

            domain = expression.AND([
                [("id", "=", self.id)],
                rule_domain,
            ])

            if self.sudo().search_count(domain):
                return rule

        return False

    def _compute_portal_cancellation_allowed(self):
        now = fields.Datetime.now()

        for order in self:
            denial_rule = order._get_portal_cancellation_denial_rule()

            order.portal_cancellation_denial_rule_id = denial_rule

            order.portal_cancellation_allowed = bool(
                order.state != "cancel"
                and not order.portal_cancellation_received
                and not order.portal_cancellation_ids
                and order.portal_cancellation_deadline
                and order.portal_cancellation_deadline >= now
                and order._has_portal_cancellable_lines()
                and not denial_rule
            )