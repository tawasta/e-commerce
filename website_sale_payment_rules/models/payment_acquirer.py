from odoo import fields, models


class PaymentAcquirer(models.Model):
    _inherit = "payment.acquirer"

    allowed_group_ids = fields.Many2many(
        string="Allowed groups", comodel_name="res.groups"
    )
