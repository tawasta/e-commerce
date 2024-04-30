from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    show_edicode_field = fields.Boolean(
        string="Show Edicode field",
        related="website_id.show_edicode_field",
        readonly=False,
    )

    show_edicode_notification = fields.Boolean(
        string="Show Edicode notification",
        related="website_id.show_edicode_notification",
        readonly=False,
    )

    show_edicode_in_address_card = fields.Boolean(
        string="Show Edicode in address card",
        related="website_id.show_edicode_in_address_card",
        readonly=False,
    )
