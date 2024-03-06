from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    website_sale_extra_step_reference = fields.Boolean(
        string="Hide reference in the extra step",
        related="website_id.website_sale_extra_step_reference",
        readonly=False,
    )

    website_sale_extra_step_info = fields.Boolean(
        string="Hide info in the extra step",
        related="website_id.website_sale_extra_step_info",
        readonly=False,
    )

    website_sale_extra_step_attachment = fields.Boolean(
        string="Hide attachment in the extra step",
        related="website_id.website_sale_extra_step_attachment",
        readonly=False,
    )
