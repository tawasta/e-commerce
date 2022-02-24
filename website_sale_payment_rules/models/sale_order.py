from odoo import models, api, fields
from odoo.tools.translate import _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        values = super(SaleOrder, self)._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        website = self.env['website'].get_current_website()
        order_line = self.env["sale.order.line"].sudo().search([
            ('id', '=', values.get('line_id'))
        ])

        if website.company_id != order_line.product_id.company_id:
            company_id = order_line.product_id.company_id
            order_line = order_line.with_company(company_id)
            fpos = order_line.order_id.fiscal_position_id or order_line.order_id.fiscal_position_id.get_fiscal_position(order_line.order_partner_id.id)
            # If company_id is set, always filter taxes by the company
            taxes = order_line.product_id.taxes_id.filtered(lambda t: t.company_id == order_line.env.company)
            tax_id = fpos.map_tax(taxes, order_line.product_id, order_line.order_id.partner_shipping_id)
            order_line.sudo().write({'tax_id': tax_id})

        return values
