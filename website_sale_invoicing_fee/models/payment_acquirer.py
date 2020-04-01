from odoo import fields
from odoo import models


class PaymentAcquirer(models.Model):

    _inherit = 'payment.acquirer'

    product_id = fields.Many2one(
        string="Extra fee product",
        comodel_name="product.product",
        help="Product is added to Sale Order when this payment is used on webshop"
    )
