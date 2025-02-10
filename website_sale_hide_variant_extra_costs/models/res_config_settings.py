from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    hide_variant_extra_costs = fields.Boolean(
        string="Hide Variant Costs from Product Page Dropdowns",
        related="company_id.hide_variant_extra_costs",
        readonly=False,
    )
