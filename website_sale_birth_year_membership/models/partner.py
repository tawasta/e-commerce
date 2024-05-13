from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    year_of_birth = fields.Integer(string="Year of Birth")
