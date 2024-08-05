from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    requires_attachment = fields.Boolean("Requires an attachment")
    requires_attachment_help = fields.Text(
        "Attachment help",
        translate=True,
        help="Show this help text if order attachment is missing",
    )
