from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCustom(WebsiteSale):
    @http.route()
    def shop(self, page=0, category=None, search="", ppg=False, **post):
        res = super(WebsiteSaleCustom, self).shop(
            page=page, category=category, search=search, ppg=ppg, **post
        )

        Category = request.env["product.public.category"]
        search_categories = False
        if search and not category:
            search_categories = Category.search([])
            categs = Category.search(
                [("parent_id", "=", False)] + request.website.website_domain()
            )
        else:
            categs = Category.search(
                [("parent_id", "=", False)] + request.website.website_domain()
            )

        if category and search:
            search_categories = Category.search([])
            categs = Category.search(
                [("parent_id", "=", False)] + request.website.website_domain()
            )

        res.qcontext.update(
            {
                "categories": categs,
                "search_categories_ids": search_categories and search_categories.ids,
            }
        )

        return res
