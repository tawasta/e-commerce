import logging

from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSaleLoginRequired(WebsiteSale):
    # Affects:
    # '/shop',
    # '/shop/page/<int:page>',
    # '/shop/category/<model("product.public.category"):category>',
    # '/shop/category/<model("product.public.category"):category>/page/<int:page>',
    @http.route(auth="user", sitemap=False)
    def shop(self, *args, **kwargs):
        return super().shop(*args, **kwargs)

    # Affects:
    # /shop/<model("product.template"):product>
    @http.route(auth="user", sitemap=False)
    def product(self, *args, **kwargs):
        return super().product(*args, **kwargs)

    # Affects:
    # '/shop/<model("product.template"):product_template>/document/<int:document_id>',
    @http.route(auth="user")
    def product_document(self, *args, **kwargs):
        return super().product_document(*args, **kwargs)

    # Affects:
    # /shop/product/<model("product.template"):product>
    @http.route(auth="user")
    def old_product(self, *args, **kwargs):
        return super().old_product(*args, **kwargs)

    # Affects:
    # /shop/cart
    @http.route(auth="user")
    def cart(self, *args, **kwargs):
        return super().cart(*args, **kwargs)

    # Affects:
    # /shop/cart/update
    @http.route(auth="user")
    def cart_update(self, *args, **kwargs):
        return super().cart_update(*args, **kwargs)

    # Affects:
    # /shop/cart/update_json
    @http.route(auth="user")
    def cart_update_json(self, *args, **kwargs):
        return super().cart_update_json(*args, **kwargs)

    # Affects:
    # /shop/address
    @http.route(auth="user")
    def address(self, *args, **kwargs):
        return super().address(*args, **kwargs)

    # Affects:
    # /shop/checkout
    @http.route(auth="user")
    def checkout(self, *args, **kwargs):
        return super().checkout(*args, **kwargs)

    # Affects:
    # /shop/extra_info
    @http.route(auth="user")
    def extra_info(self, *args, **kwargs):
        return super().extra_info(*args, **kwargs)

    # Affects:
    # /shop/payment
    @http.route(auth="user")
    def shop_payment(self, *args, **kwargs):
        return super().shop_payment(*args, **kwargs)

    # Affects:
    # /shop/payment/validate
    @http.route(auth="user")
    def shop_payment_validate(self, *args, **kwargs):
        return super().shop_payment_validate(*args, **kwargs)

    # Affects:
    # /shop/confirmation
    @http.route(auth="user")
    def shop_payment_confirmation(self, *args, **kwargs):
        return super().shop_payment_confirmation(*args, **kwargs)

    # Affects:
    # /shop/change_pricelist/<model("product.pricelist"):pricelist>
    @http.route(auth="user")
    def pricelist_change(self, *args, **kwargs):
        return super().pricelist_change(*args, **kwargs)

    # Affects:
    # /shop/pricelist
    @http.route(auth="user")
    def pricelist(self, *args, **kwargs):
        return super().pricelist(*args, **kwargs)

    # Affects:
    # /shop/confirm_order
    @http.route(auth="user")
    def confirm_order(self, *args, **kwargs):
        return super().confirm_order(*args, **kwargs)

    # Affects:
    # '/shop/print'
    @http.route(auth="user")
    def print_saleorder(self, *args, **kwargs):
        return super().print_saleorder(*args, **kwargs)
