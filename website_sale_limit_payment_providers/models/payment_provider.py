from odoo import fields, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    website_show_company = fields.Boolean(
        string="Visible for companies",
        default=True,
        help="If partner is company type or has VAT-code, it's treated as a company",
    )

    website_show_private = fields.Boolean(
        string="Visible for private customers",
        default=True,
        help="If partner is not company type and has no VAT-code, it's treated as a private customer",
    )
