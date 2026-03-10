from odoo import fields, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    website_show_company = fields.Boolean(
        string="Visible for companies",
        default=True,
        help="If partner is company type or has VAT-code, " "it's treated as a company",
    )

    website_show_private = fields.Boolean(
        string="Visible for private customers",
        default=True,
        help="If partner is not company type and has no VAT-code, "
        "it's treated as a private customer",
    )

    website_show_for_group_ids = fields.Many2many(
        comodel_name="res.groups",
        string="Visible for only customers in groups",
        help="Use to e.g. limit invoice-based paying only to signed in (portal) "
        "users. If field is left empty, payment provider is shown for all groups' "
        "users.",
    )
