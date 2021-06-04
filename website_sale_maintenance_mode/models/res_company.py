from odoo import fields
from odoo import models


class Company(models.Model):
    _inherit = "res.company"

    website_sale_maintenance_text = fields.Html('Website sale maintenance text')
