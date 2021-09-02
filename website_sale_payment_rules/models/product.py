from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    payment_only_invoice = fields.Boolean("Payment by invoice only")
