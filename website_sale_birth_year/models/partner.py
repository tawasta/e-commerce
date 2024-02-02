from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    birth_year = fields.Many2one(string="Birth year", comodel_name="res.birth.year")
