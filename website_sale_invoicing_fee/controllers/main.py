from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
from odoo.http import route


class InvoicingFee(WebsiteSale):

    @route()
    def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
        sale_order = request.website.sale_get_order() or False

        line_product_id = sale_order and \
            sale_order.transaction_ids.acquirer_id.product_id or \
            False

        sale_order_line_model = request.env['sale.order.line']

        if line_product_id and sale_order:
            product_desc = '{}{}'.format(
                line_product_id.default_code and '[{}] '.format(
                    line_product_id.default_code) or '', line_product_id.name)

            sale_order_line_model.sudo().create({
                'customer_lead': 0,
                'product_id': line_product_id.id,
                'product_uom_qty': 1,
                'price_unit': line_product_id.list_price,
                'name': product_desc,
                'order_id': sale_order.id,
            })

        return super(InvoicingFee, self).payment_validate(transaction_id,
                                                          sale_order_id, **post)
