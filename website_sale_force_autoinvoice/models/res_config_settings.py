from odoo import fields
from odoo import models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    create_invoice = fields.Boolean(
        string="Shop confirmation: create invoice",
        config_parameter="website_sale_force_autoinvoice.create_invoice",
    )
