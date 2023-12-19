from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    allow_selecting_sibling_billing_addresses = fields.Boolean(
        string="Allow Selecting Sibling Billing Addresses",
        related="website_id.allow_selecting_sibling_billing_addresses",
        readonly=False,
        help="Let the customer select also from those billing addressed that are not "
        "directly linked to the customer but belong to the same parent company.",
    )
