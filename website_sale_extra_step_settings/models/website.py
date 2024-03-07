from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    website_sale_extra_step_reference = fields.Boolean(
        string="Hide reference in the extra step",
    )

    website_sale_extra_step_info = fields.Boolean(
        string="Hide info in the extra step",
    )

    website_sale_extra_step_attachment = fields.Boolean(
        string="Hide attachment in the extra step",
    )
