from odoo import fields, models


class Website(models.Model):

    _inherit = "website"

    allow_selecting_sibling_billing_addresses = fields.Boolean(
        string="Allow Selecting Sibling Billing Addresses",
        default=False,
        help="Let the customer select also from those billing addressed that are not "
        "directly linked to the customer but belong to the same parent company.",
    )
