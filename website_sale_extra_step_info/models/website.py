from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    extra_step_text = fields.Html(
        string="Website sale extra step: info text", readonly=False, translate=True
    )
