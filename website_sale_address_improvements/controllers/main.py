from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCustom(WebsiteSale):

    @http.route(['/shop/confirmation'],
                type='http', auth="public", website=True)
    def payment_confirmation(self, **post):
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            # If the portal user who placed the order is an individual,
            # link the order to their parent company.
            # onchange is not called, so the selected shipping address is
            # maintained, as is the invoice address (computed in core with
            # address_get)
            if not order.partner_id.is_company \
                    and order.partner_id.parent_id \
                    and order.partner_id.parent_id.is_company:

                order.partner_id = order.partner_id.parent_id.id

        return super(WebsiteSaleCustom, self).payment_confirmation(**post)
