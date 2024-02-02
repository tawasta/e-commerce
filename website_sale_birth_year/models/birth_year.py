from odoo import fields, models


class ResBirthYear(models.Model):
    _name = "res.birth.year"

    name = fields.Char(string="Name")
