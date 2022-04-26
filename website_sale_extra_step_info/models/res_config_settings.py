from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    website_sale_extra_step_text = fields.Html(
        string="Website sale extra step: info text",
        related="website_id.extra_step_text",
        readonly=False,
        translate=True,
    )
