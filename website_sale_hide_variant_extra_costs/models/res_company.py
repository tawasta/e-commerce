from odoo import fields, models


class ResCompany(models.Model):

    _inherit = "res.company"

    hide_variant_extra_costs = fields.Boolean(
        string="Hide Variant Costs from Product Page Dropdowns",
    )
