from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
from odoo import http


class WebsiteEventSale(WebsiteSale):
    @http.route(
        "/shop/payment/validate",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def shop_payment_validate(self, sale_order_id=None, **post):
        # Selvitetään tilaus ennen superin kutsua
        if sale_order_id:
            order = request.env["sale.order"].sudo().browse(sale_order_id)
        else:
            order = request.website.sale_get_order()
            if not order and "sale_last_order_id" in request.session:
                last_order_id = request.session["sale_last_order_id"]
                order = request.env["sale.order"].sudo().browse(last_order_id).exists()

        # Käytetään ensimmäistä transaktiota lisätäksemme laskutustuotteen
        if order and order.transaction_ids:
            transaction = order.transaction_ids[0]
            product = transaction.payment_method_id.product_id
            if product:
                # Tarkista onko tuote jo olemassa tilauksella, ettei tule duplikaatteja
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

        # Palauta superin logiikka normaalisti
        return super().shop_payment_validate(sale_order_id=sale_order_id, **post)
