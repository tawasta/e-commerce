from odoo import api
from odoo import models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def action_quotation_send(self):
        sale_transactions = self.transaction_ids and \
            self.transaction_ids[0]

        line_product_id = self and \
            sale_transactions.acquirer_id.product_id or \
            False

        sale_order_line_model = self.env['sale.order.line']

        current_website = self.env['website'].get_current_website()

        if line_product_id and self:
            product_desc = '{}{}'.format(
                line_product_id.default_code and '[{}] '.format(
                    line_product_id.default_code) or '',
                line_product_id.name)

            sale_order_line_model.sudo().create({
                'customer_lead': 0,
                'product_id': line_product_id.id,
                'product_uom_qty': 1,
                'price_unit': line_product_id.list_price,
                'name': product_desc,
                'order_id': self.id,
                'company_id': current_website.id,
            })

        return super(SaleOrder, self).action_quotation_send()
