from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleProductCode(WebsiteSale):

    @http.route(['/shop/get_variant_code/'], type='json', auth='public',
                website=True)
    def get_variant_code(self, **post):
        product_id = post.get('product_id', False)
        if product_id:
            args = [('id', '=', product_id)]
            product = request.env['product.product'].search(args=args, limit=1)

            return {
                'code': product.default_code or '-'
            }
        else:
            return {}
