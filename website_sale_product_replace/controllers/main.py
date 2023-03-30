from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import TableCompute, WebsiteSale


class WebsiteSaleReplace(WebsiteSale):
    @http.route()
    def shop(self, page=0, category=None, search="", ppg=False, **post):
        res = super(WebsiteSaleReplace, self).shop(page, category, search, ppg, **post)

        if request.env.user.has_group("website.group_website_publisher"):
            # Editors will see all products, without replacements
            return res

        products = res.qcontext.get("products", {})

        customer_products = self._get_customer_products(products)

        if ppg:
            try:
                ppg = int(ppg)
                post["ppg"] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env["website"].get_current_website().shop_ppg or 20

        ppr = request.env["website"].get_current_website().shop_ppr or 4

        res.qcontext["products"] = customer_products
        res.qcontext["bins"] = TableCompute().process(customer_products, ppg, ppr)

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

            # Search for published replacement products
            replacement_domain = [
                ("replace_product_id", "=", product.id),
                ("website_published", "=", True),
            ]
            replacement_products = product.sudo().search(replacement_domain)

            for replacement in replacement_products:
                # TODO: handle multiple matching replacements
                customer_ids = replacement.sudo().customer_ids

                if not customer_ids or customer in customer_ids:
                    # Replace product for this customer
                    product = replacement

            if product.id not in product_ids:
                product_ids.append(product.id)

        customer_products = request.env["product.template"].browse(product_ids)

        return customer_products

    @http.route()
    def product(self, product, category="", search="", **kwargs):
        replacement = self._get_customer_products(product)

        if replacement and replacement != product:
            return request.redirect("/shop/product/%s" % replacement.id)

        return super(WebsiteSaleReplace, self).product(
            product, category, search, **kwargs
        )
