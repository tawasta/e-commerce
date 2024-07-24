from odoo import fields, models


class PaymentProvider(models.Model):

    _inherit = "payment.provider"

    auto_confirm = fields.Selection(
        [("allow", "Allow"), ("not_allowed", "Not allowed")], default="not_allowed"
    )

    auto_create_invoice = fields.Selection(
        [("allow", "Allow"), ("not_allowed", "Not allowed")], default="not_allowed"
    )
