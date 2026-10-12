import logging

from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSalePaymentProviders(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super()._get_shop_payment_values(order, **kwargs)
        _logger.info(
            "DEBUG limit_providers order=%s company=%s website=%s user=%s core=%s",
            order.id,
            order.company_id.id,
            request.website.id,
            request.env.user.id,
            values["providers_sudo"].ids,
        )

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

        _logger.info(
            "DEBUG limit_providers product_limits=%s",
            [
                (li.product_id.id, li.product_id.allowed_payment_provider_ids.ids)
                for li in order.order_line
                if not li.display_type and li.product_id
            ],
        )
        if allowed_providers_list:
            common_providers = set.intersection(*allowed_providers_list)
            if not common_providers:
                values["providers_sudo"] = PaymentProvider
                values["payment_methods_sudo"] = PaymentMethod
                return values

            providers_sudo = (providers_sudo | explicit_allowed_providers).filtered(
                lambda p: p.id in common_providers
            )

        _logger.info("DEBUG limit_providers after_product_limit=%s", providers_sudo.ids)
        invoice_companies = order.order_line.filtered(
            lambda line: (
                not line.display_type
                and line.product_id
                and line.product_id.invoice_company_id
            )
        ).mapped("product_id.invoice_company_id")

        _logger.info(
            "DEBUG limit_providers invoice_companies=%s order_company=%s",
            invoice_companies.ids,
            order.company_id.id,
        )
        if len(invoice_companies) == 1 and invoice_companies != order.company_id:
            providers_sudo = PaymentProvider._get_compatible_providers(
                invoice_companies.id,
                order.partner_id.id,
                order.amount_total - order.amount_paid,
                currency_id=order.currency_id.id,
                sale_order_id=order.id,
                website_id=request.website.id,
            )

        _logger.info(
            "DEBUG limit_providers after_invoice_company=%s", providers_sudo.ids
        )
        if len(invoice_companies) > 1:
            providers_sudo = providers_sudo.filtered(
                lambda p: p.website_allow_mixed_variant_companies
            )

        is_company = order.partner_invoice_id.is_company or order.partner_invoice_id.vat
        _logger.info(
            "DEBUG limit_providers after_mixed=%s is_company=%s",
            providers_sudo.ids,
            bool(is_company),
        )

        if is_company:
            providers_sudo = providers_sudo.filtered(lambda p: p.website_show_company)
        else:
            providers_sudo = providers_sudo.filtered(lambda p: p.website_show_private)

        _logger.info("DEBUG limit_providers after_customer_type=%s", providers_sudo.ids)
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
        _logger.info(
            "DEBUG limit_providers final providers=%s methods=%s",
            providers_sudo.ids,
            values["payment_methods_sudo"].ids,
        )

        return values
