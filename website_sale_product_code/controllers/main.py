from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    @http.route(
        '/product/get/default_code',
        type='json',
        auth='public',
        website=True)
    def products_get(self, **post):
        code = ""
        if post.get('id'):
            product_model = request.env['product.product']
            domain = [
                ('website_published', '=', True),
                ('id', '=', post.get('id')),
            ]

            product = product_model.search_read(
                domain,
                ['default_code'],
            )

            if product:
                code = product[0]['default_code']

        return code
