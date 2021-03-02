from odoo import _
from odoo import api
from odoo import fields
from odoo import models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def action_quotation_send(self):
        if self.transaction_ids.acquirer_id.auto_confirm == 'allow':
            self.sudo().action_confirm()

        return super(SaleOrder, self).action_quotation_send()
