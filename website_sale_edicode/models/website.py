from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    show_edicode_field = fields.Boolean(
        string="Show Edicode field",
    )

    show_edicode_notification = fields.Boolean(
        string="Show Edicode notification",
    )

    show_edicode_in_address_card = fields.Boolean(
        string="Show Edicode in address card",
    )
