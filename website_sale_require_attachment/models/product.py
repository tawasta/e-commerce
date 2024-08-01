from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    requires_attachment = fields.Boolean("Requires an attachment")
