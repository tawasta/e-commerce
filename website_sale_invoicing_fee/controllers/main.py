from odoo.http import request

from odoo.addons.payment.controllers import portal as payment_portal


class PaymentPortal(payment_portal.PaymentPortal):
    def _create_transaction(
        self, *args, payment_method_id=None, token_id=None, **kwargs
    ):
        tx_sudo = super()._create_transaction(
            *args,
            payment_method_id=payment_method_id,
            token_id=token_id,
            **kwargs,
        )

        # request.cart is only set for frontend (website=True) dispatches
        # (see website_sale's IrHttp._frontend_pre_dispatch); other callers
        # of _create_transaction, e.g. portal invoice payments, never set it.
        order = getattr(request, "cart", False)
        if not order:
            return tx_sudo

        payment_method = self._get_selected_payment_method(payment_method_id, token_id)
        order.payment_method_id = payment_method.id  # request.cart is already sudoed
        # sale.order.write() picks the field change up and (re)syncs the fee
        # line automatically; see sale_invoicing_fee's SaleOrder.write().

        return tx_sudo

    def _get_selected_payment_method(self, payment_method_id, token_id):
        """The payment method behind the customer's choice: either the one
        picked directly, or the one behind the saved token they reused."""
        if payment_method_id:
            return request.env["payment.method"].sudo().browse(payment_method_id)
        if token_id:
            token = request.env["payment.token"].sudo().browse(token_id)
            return token.payment_method_id
        return request.env["payment.method"]
