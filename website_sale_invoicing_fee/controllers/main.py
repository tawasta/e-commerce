from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request


class WebsiteEventSale(WebsiteSale):
    def _prepare_shop_payment_confirmation_values(self, order):
        values = super()._prepare_shop_payment_confirmation_values(order)

        # Lisätään laskutustuote (invoicing fee) tilaukseen
        if order and order.transaction_ids:
            transaction = order.transaction_ids[0]
            product = transaction.payment_method_id.product_id
            if product:
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

        return values
