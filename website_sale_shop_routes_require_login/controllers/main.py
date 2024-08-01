import logging

from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSaleLoginRequired(WebsiteSale):

    # Affects:
    # /shop
    # /shop/page/<int:page>
    # /shop/category/<model("product.public.category"):category>
    # /shop/category/<model("product.public.category"):category>/page/<int:page>
    @http.route(auth="user", sitemap=False)
    def shop(self, page=0, category=None, search="", ppg=False, **post):
        return super().shop(page, category, search, ppg, **post)

    # Affects:
    # /shop/<model("product.template"):product>
    @http.route(auth="user", sitemap=False)
    def product(self, product, category="", search="", **kwargs):
        return super().product(product, category, search, **kwargs)

    # Affects:
    # /shop/product/<model("product.template"):product>
    @http.route(auth="user")
    def old_product(self, product, category="", search="", **kwargs):
        return super().old_product(product, category, search, **kwargs)

    # Affects:
    # /shop/cart
    @http.route(auth="user")
    def cart(self, access_token=None, revive="", **post):
        return super().cart(access_token, revive, **post)

    # Affects:
    # /shop/address
    @http.route(auth="user")
    def address(self, **kw):
        return super().address(**kw)

    # Affects:
    # /shop/checkout
    @http.route(auth="user")
    def checkout(self, **post):
        return super().checkout(**post)

    # Affects:
    # /shop/extra_info
    @http.route(auth="user")
    def extra_info(self, **post):
        return super().extra_info(**post)

    # Affects:
    # /shop/payment
    @http.route(auth="user")
    def payment(self, **post):
        return super().payment(**post)

    # Affects:
    # /shop/confirmation
    @http.route(auth="user")
    def payment_confirmation(self, **post):
        return super().payment_confirmation(**post)

    # Affects:
    # /shop/change_pricelist/<model("product.pricelist"):pl_id>
    @http.route()
    def pricelist_change(self, pl_id, **post):
        return super().pricelist_change(pl_id, **post)

    # Affects:
    # /shop/pricelist
    @http.route()
    def pricelist(self, promo, **post):
        return super().pricelist(promo, **post)

    # Affects:
    # /shop/confirm_order
    @http.route()
    def confirm_order(self, **post):
        return super().confirm_order(**post)
