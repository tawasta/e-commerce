from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute


class WebsiteSaleReplace(WebsiteSale):

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res = super(WebsiteSaleReplace, self).shop(
            page, category, search, ppg, **post
        )

        products = res.qcontext.get('products', {})
        customer_products = self._get_customer_products(products)

        res.qcontext['products'] = customer_products
        res.qcontext['bins'] = TableCompute().process(customer_products, ppg)

        return res

    def _get_customer_products(self, products):
        # Check the products that are about to be rendered whether the
        # product should be replaced with a customer-specific one
        product_ids = []
        contact = request.env.user.partner_id
        customer = contact.commercial_partner_id

        for product in products:
            product_sudo = product.sudo()
            if product_sudo.replacement_ids:
                # Don't add replacement products
                continue

            if product.replace_product_id:
                customer_ids = product_sudo.customer_ids

                if not customer_ids or customer in customer_ids:
                    # Replace product for this customer
                    product = product.replace_product_id

            if product.id not in product_ids:
                if product.website_published:
                    product_ids.append(product.id)

        customer_products = request.env['product.template'].browse(product_ids)

        return customer_products
