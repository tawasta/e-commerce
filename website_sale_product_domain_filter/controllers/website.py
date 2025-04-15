# -*- coding: utf-8 -*-
import logging

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website

_logger = logging.getLogger(__name__)


class WebsitePaywall(Website):
    @http.route()
    def autocomplete(self, search_type=None, term=None, order=None, limit=5, max_nb_chars=999, options=None):
        response = super().autocomplete(search_type, term, order, limit, max_nb_chars, options)

        if search_type == "products" and isinstance(response, dict) and "results" in response:
            filtered_results = []
            for product in response["results"]:
                url = str(product.get("website_url", ""))
                # Poimi ID URL:sta, esim. "/shop/subscription-aaa-3" → id = 3
                try:
                    product_id = int(url.strip("/").split("-")[-1])
                except Exception:
                    continue  # Ei kelvollinen ID

                tmpl = request.env['product.template'].browse(product_id)
                if tmpl.exists() and (not tmpl.paywall_domain or tmpl.user_in_paywall_domain):
                    filtered_results.append(product)

            response["results"] = filtered_results
        return response
