from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    payment_only_invoice = fields.Boolean("Payment by invoice only")

    requires_attachment = fields.Boolean("Requires an attachment")

    requires_explanation = fields.Boolean("Requires an explanation")

    company_id = fields.Many2one(
        'res.company', 'Company', index=1, required=True)
