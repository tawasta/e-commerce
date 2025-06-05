import logging

from odoo import http
from odoo.http import request
from odoo.osv import expression

from odoo.addons.website_sale.controllers.main import WebsiteSale
from werkzeug.exceptions import NotFound

_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):
    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        fuzzy_search_term, product_count, search_result = super()._shop_lookup_products(
            attrib_set, options, post, search, website
        )

        # Suodata tuotteet: näytä jos käyttäjällä on pääsy
        filtered_products = search_result.filtered(lambda p: p.user_in_partner_domain)

        return fuzzy_search_term, len(filtered_products), filtered_products

    @http.route([])
    def product(self, product, category="", search="", **kwargs):
        """Yksittäisen tuotteen näkymä — estä pääsy jos ei oikeuksia"""
        if not product.user_in_partner_domain:
            raise NotFound()
        return super().product(product, category=category, search=search, **kwargs)
