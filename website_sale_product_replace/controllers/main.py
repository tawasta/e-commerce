from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website_sale.controllers.main import PPG


class WebsiteSaleReplace(WebsiteSale):

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res = super(WebsiteSaleReplace, self).shop(
            page, category, search, ppg, **post
        )

        if request.env.user.has_group('website.group_website_publisher'):
            # Editors will see all products, without replacements
            return res

        products = res.qcontext.get('products', {})

        customer_products = self._get_customer_products(products)

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

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
            if product.replace_product_id:
                # Don't show replacement products themselves
                continue

            for replacement in product.replacement_ids:
                # TODO: handle multiple matching replacements
                customer_ids = replacement.sudo().customer_ids

                if not customer_ids or customer in customer_ids:
                    # Replace product for this customer
                    product = replacement

            if product.id not in product_ids:
                if product.website_published:
                    product_ids.append(product.id)

        customer_products = request.env['product.template'].browse(product_ids)

        return customer_products

    @http.route()
    def product(self, product, category='', search='', **kwargs):
        replacement = self._get_customer_products(product)

        if replacement and replacement != product:
            return request.redirect('/shop/product/%s' % replacement.id)

        return super(WebsiteSaleReplace, self).product(
            product, category, search, **kwargs
        )
