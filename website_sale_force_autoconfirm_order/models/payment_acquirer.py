# coding: utf-8
from odoo import models, fields, _


class PaymentAcquirer(models.Model):

    _inherit = 'payment.acquirer'

    auto_confirm = fields.Selection(
        selection_add=[('force_confirm',
                        _('Ignore authorization and confirm SO immediately'))]
    )
