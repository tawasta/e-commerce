from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    allowed_payment_provider_ids = fields.Many2many(
        string="Allowed payment providers",
        help="Leaving this empty will allow any provider to be used",
        comodel_name="payment.provider",
        domain=[("state", "in", ["enabled", "test"])],
    )
