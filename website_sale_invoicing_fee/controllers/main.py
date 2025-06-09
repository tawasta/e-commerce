from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request, route
import logging

_logger = logging.getLogger(__name__)


class WebsiteEventSale(WebsiteSale):
    @route(["/shop/payment"], type="http", auth="public", website=True, sitemap=False)
    def shop_payment(self, **post):
        order = request.website.sale_get_order()

        # Jatketaan vain jos tilaus on olemassa
        if order and post:
            _logger.info("===POST==== %s", post)
            # Haetaan mahdollinen olemassa oleva transaktio
            transaction = order.transaction_ids.filtered(
                lambda t: t.state in ("draft", "pending")
            )
            _logger.info("===TRANSACTION=== %s", transaction)
            if transaction:
                payment_method = transaction[0].payment_method_id
                product = payment_method.product_id
                if product and not any(
                    line.product_id.id == product.id for line in order.order_line
                ):
                    # Lisää laskutustuote tilaukseen
                    product_desc = (
                        f"[{product.default_code}] {product.name}"
                        if product.default_code
                        else product.name
                    )
                    request.env["sale.order.line"].sudo().create(
                        {
                            "order_id": order.id,
                            "product_id": product.id,
                            "name": product_desc,
                            "product_uom_qty": 1,
                            "price_unit": product.list_price,
                            "company_id": order.company_id.id,
                        }
                    )

        # Lopuksi jatketaan alkuperäisellä logiikalla
        return super().shop_payment(**post)
