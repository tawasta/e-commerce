from odoo import fields, models


class Partner(models.Model):

    _inherit = "res.partner"

    skip_website_checkout_payment = fields.Boolean(default=True)
