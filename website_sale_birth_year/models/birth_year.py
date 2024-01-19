from odoo import models, fields

class ResBirthYear(models.Model):
    _name = 'res.birth.year'

    name = fields.Char(string='Name')

