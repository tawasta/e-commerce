from odoo import http, _
from odoo.exceptions import MissingError, AccessError, ValidationError
from odoo.http import request
from odoo.addons.payment.controllers import portal as payment_portal
from odoo import tools
from odoo import Command
import logging

_logger = logging.getLogger(__name__)


class PaymentPortal(payment_portal.PaymentPortal):
    @http.route()
    def shop_payment_transaction(self, order_id, access_token, **kwargs):
        # Haetaan tilaus ja tarkistetaan access
        _logger.info(
            f"shop_payment_transaction called with order_id={order_id}, access_token={access_token}, kwargs={kwargs}"
        )

        try:
            order = self._document_check_access("sale.order", order_id, access_token)
        except MissingError as error:
            raise error
        except AccessError:
            raise ValidationError(_("The access token is invalid."))

        if order.state == "cancel":
            raise ValidationError(_("The order has been canceled."))

        order._check_cart_is_ready_to_be_paid()

        # Lisätään se oma lisäys ennen super-kutsua:
        payment_method_id = kwargs.get("payment_method_id")
        if payment_method_id:
            product = (
                request.env["payment.method"]
                .sudo()
                .browse(int(payment_method_id))
                .product_id
            )
            if product and not any(
                line.product_id.id == product.id for line in order.order_line
            ):
                product_desc = (
                    f"[{product.default_code}] {product.name}"
                    if product.default_code
                    else product.name
                )
                request.env["sale.order.line"].sudo().create(
                    {
                        "order_id": order.id,
                        "product_id": product.id,
                        "product_uom_qty": 1,
                        "price_unit": product.list_price,
                        "name": product_desc,
                        "company_id": order.company_id.id,
                    }
                )

        # Kutsutaan alkuperäisen luokan metodia
        result = super().shop_payment_transaction(order_id, access_token, **kwargs)
        _logger.info(f"Super call returned: {result}")
        return result
