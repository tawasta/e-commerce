from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleAttributeDependency(WebsiteSale):

    @http.route(
        '/attribute/value/get/dependencies',
        type='json',
        auth='public',
        website=True)
    def attribute_value_get_dependencies(self, **post):
        attributes = []

        if post.get('id'):
            pav_model = request.env['product.attribute.value']
            domain = [
                ('id', '=', int(post.get('id'))),
            ]

            res = pav_model.search_read(
                domain,
                ['dependent_attribute_ids'],
            )

            if res:
                attributes = res[0]['dependent_attribute_ids']

        return attributes
