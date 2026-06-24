from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSalePaymentProviders(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super()._get_shop_payment_values(order, **kwargs)

        PaymentProvider = request.env["payment.provider"].sudo()
        PaymentMethod = request.env["payment.method"].sudo()

        providers_sudo = values["providers_sudo"]
        order = order.sudo()

        allowed_providers_list = []
        explicit_allowed_providers = PaymentProvider

        for line in order.order_line.filtered(
            lambda li: not li.display_type and li.product_id
        ):
            allowed = line.product_id.allowed_payment_provider_ids.sudo()
            if allowed:
                allowed_providers_list.append(set(allowed.ids))
                explicit_allowed_providers |= allowed

        if allowed_providers_list:
            common_providers = set.intersection(*allowed_providers_list)
            if not common_providers:
                values["providers_sudo"] = PaymentProvider
                values["payment_methods_sudo"] = PaymentMethod
                return values

            providers_sudo = (providers_sudo | explicit_allowed_providers).filtered(
                lambda p: p.id in common_providers
            )

        variant_companies = order.order_line.filtered(
            lambda line: (
                not line.display_type
                and line.product_id
                and line.product_id.variant_company_id
            )
        ).mapped("product_id.variant_company_id")

        if len(variant_companies) > 1:
            providers_sudo = providers_sudo.filtered(
                lambda p: p.website_allow_mixed_variant_companies
            )

        is_company = order.partner_invoice_id.is_company or order.partner_invoice_id.vat

        if is_company:
            providers_sudo = providers_sudo.filtered(lambda p: p.website_show_company)
        else:
            providers_sudo = providers_sudo.filtered(lambda p: p.website_show_private)

        current_user_groups = request.env.user.groups_id

        providers_sudo = providers_sudo.filtered(
            lambda p: not p.website_show_for_group_ids
            or bool(p.website_show_for_group_ids & current_user_groups)
        )

        values["providers_sudo"] = providers_sudo
        values["payment_methods_sudo"] = PaymentMethod._get_compatible_payment_methods(
            providers_sudo.ids,
            order.partner_id.id,
            currency_id=order.currency_id.id,
        )

        return values
