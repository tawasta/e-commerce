from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
from odoo import http


class WebsiteEventSale(WebsiteSale):

    @http.route('/shop/payment', type='http', auth='public', website=True, sitemap=False)
    def shop_payment(self, **post):
        order = request.website.sale_get_order()

        # Laskutustuotteen lisäys VAIN POST-pyynnöillä
        if request.httprequest.method == 'POST' and order:
            transaction = order.transaction_ids[0]
            product = transaction.payment_method_id.product_id
            if product:
                existing_product_ids = order.order_line.mapped("product_id").ids
                if product.id not in existing_product_ids:
                    product_desc = (
                        f"[{product.default_code}] {product.name}"
                        if product.default_code
                        else product.name
                    )
                    request.env["sale.order.line"].sudo().create(
                        {
                            "customer_lead": 0,
                            "product_id": product.id,
                            "product_uom_qty": 1,
                            "price_unit": product.list_price,
                            "name": product_desc,
                            "order_id": order.id,
                            "company_id": request.website.company_id.id,
                        }
                    )

        # Palautetaan superin normaali logiikka
        return super().shop_payment(**post)
