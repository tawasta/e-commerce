from odoo import _
from odoo import fields
from odoo import models


class PaymentAcquirer(models.Model):

    _inherit = 'payment.acquirer'

    auto_confirm = fields.Selection([('allow', 'Allow'), ('not_allowed', 'Not allowed')], default='not_allowed')

    create_invoice = fields.Selection([('allow', 'Allow'), ('not_allowed', 'Not allowed')], default='not_allowed')
