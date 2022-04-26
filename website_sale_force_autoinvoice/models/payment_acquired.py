from odoo import fields, models


class PaymentAcquirer(models.Model):

    _inherit = "payment.acquirer"

    auto_confirm = fields.Selection(
        [("allow", "Allow"), ("not_allowed", "Not allowed")], default="not_allowed"
    )

    auto_create_invoice = fields.Selection(
        [("allow", "Allow"), ("not_allowed", "Not allowed")], default="not_allowed"
    )
