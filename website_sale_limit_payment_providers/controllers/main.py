from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSalePaymentProviders(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super()._get_shop_payment_values(order, **kwargs)

        payment_provider = request.env["payment.provider"].sudo()
        providers_sudo = values["providers_sudo"]

        for line in order.order_line:
            # If there is no limit on allowed providers, do nothing
            if line.product_id.allowed_payment_provider_ids:
                # Exclude providers that are missing from allowed providers

                providers_list = [
                    x
                    for x in providers_sudo
                    if x in line.product_id.allowed_payment_provider_ids
                ]
                providers_sudo += next(iter(providers_list), payment_provider)

        if providers_sudo != values["providers_sudo"]:
            payment_method = request.env["payment.method"].sudo()

            payment_methods_sudo = payment_method._get_compatible_payment_methods(
                providers_sudo.ids,
                order.partner_id.id,
                currency_id=order.currency_id.id,
            )
            values["providers_sudo"] = providers_sudo
            values["payment_methods_sudo"] = payment_methods_sudo

        return values
