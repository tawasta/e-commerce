from odoo import models, fields


class PrivacyActivity(models.Model):
    _inherit = "privacy.activity"

    default_in_website_sale = fields.Boolean(
        default=False, string="Default value in website sale form", readonly=False,
    )
