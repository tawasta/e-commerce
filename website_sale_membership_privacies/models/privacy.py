from odoo import models, fields


class PrivacyActivity(models.Model):
    _inherit = "privacy.activity"

    default_in_website_sale_membership = fields.Boolean(
        default=False, string="Membership: default privacy in website sale form", readonly=False,
    )
