# coding: utf-8
from odoo import models
from odoo.tools import float_compare
import logging

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):

    _inherit = 'payment.transaction'

    def _confirm_so(self, acquirer_name=False):
        # Do the core checks first whether the related SO should get
        # confirmed. Afterwards check if the acquirer has the new force confirm
        # mode selected. If yes, confirm the order.

        res = super(PaymentTransaction, self)._confirm_so(acquirer_name)

        for tx in self:
            if tx.sale_order_id and tx.sale_order_id.state \
                    in ['draft', 'sent']:
                amount_matches \
                    = float_compare(tx.amount,
                                    tx.sale_order_id.amount_total, 2) == 0
                if amount_matches:
                    if not acquirer_name:
                        acquirer_name = tx.acquirer_id.provider or 'unknown'
                    if tx.acquirer_id.auto_confirm == 'force_confirm':
                        _logger.info('<%s> force confirming order %s (ID %s)',
                                     acquirer_name,
                                     tx.sale_order_id.name,
                                     tx.sale_order_id.id)
                    
                        tx.sale_order_id.with_context(send_email=True) \
                            .action_confirm()

        return res
