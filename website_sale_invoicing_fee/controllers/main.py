from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.payment.controllers import portal as payment_portal
import logging

_logger = logging.getLogger(__name__)


class PortalWebsiteSale(payment_portal.PaymentPortal):
    def _create_transaction(
        self,
        provider_id,
        payment_method_id,
        token_id,
        amount,
        currency_id,
        partner_id,
        flow,
        tokenization_requested,
        landing_route,
        reference_prefix=None,
        is_validation=False,
        custom_create_values=None,
        **kwargs,
    ):
        # Haetaan order custom_create_valuesista
        order = None
        if custom_create_values and "sale_order_ids" in custom_create_values:
            sale_order_ids = custom_create_values.get("sale_order_ids")
            # sale_order_ids voi olla esim [(6, 0, [order_id])]
            if sale_order_ids and isinstance(sale_order_ids, (list, tuple)):
                # Otetaan ensimmäinen order_id listasta
                order_ids = []
                # Etsitään ID:t listasta esim. [(6, 0, [38])] -> [38]
                for cmd in sale_order_ids:
                    if (
                        isinstance(cmd, (list, tuple))
                        and len(cmd) == 3
                        and isinstance(cmd[2], (list, tuple))
                    ):
                        order_ids.extend(cmd[2])
                if order_ids:
                    order = request.env["sale.order"].sudo().browse(order_ids[0])
                    if not order.exists():
                        order = None

        if order:
            payment_method = (
                request.env["payment.method"].browse(payment_method_id)
                if payment_method_id
                else None
            )
            product = payment_method.product_id if payment_method else None

            if product:
                existing_line = any(
                    line.product_id.id == product.id for line in order.order_line
                )
                if not existing_line:
                    company_id = request.env.company.id
                    request.env["sale.order.line"].sudo().create(
                        {
                            "product_id": product.id,
                            "product_uom_qty": 1,
                            "price_unit": product.list_price,
                            "name": product.name,
                            "order_id": order.id,
                            "company_id": company_id,
                        }
                    )
            amount = order.amount_total

        # Lopuksi kutsutaan alkuperäinen metodi
        return super()._create_transaction(
            provider_id,
            payment_method_id,
            token_id,
            amount,
            currency_id,
            partner_id,
            flow,
            tokenization_requested,
            landing_route,
            reference_prefix=reference_prefix,
            is_validation=is_validation,
            custom_create_values=custom_create_values,
            **kwargs,
        )
