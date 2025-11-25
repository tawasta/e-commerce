import logging

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSaleBilling(WebsiteSale):
    def _get_mandatory_fields_billing(self, country_id=False):
        """Poista sähköposti pakollisista laskutuskentistä"""
        res = super()._get_mandatory_fields_billing(country_id)
        if "email" in res:
            res.remove("email")
        return res

    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super().checkout_form_validate(
            mode, all_form_values, data
        )

        Partner = request.env["res.partner"]
        country_id = int(data.get("country_id") or 0)
        vat = data.get("billing_company_registry")

        if vat and hasattr(Partner, "check_vat") and country_id:
            vat_fixed = Partner.fix_eu_vat_number(country_id, vat)
            data["billing_company_registry"] = vat_fixed
            partner_dummy = Partner.new(
                {
                    "vat": vat_fixed,
                    "country_id": country_id,
                }
            )
            try:
                partner_dummy.sudo().check_vat()
            except ValidationError as e:
                error["billing_company_registry"] = "error"
                error_message.append(e.args[0])

        return error, error_message

    @http.route()
    def address(self, **kw):
        order = request.website.sale_get_order()

        # Säilytä arvot ennen validointia
        billing_company_registry = kw.get("billing_company_registry")
        customer_invoice_transmit_method_id = kw.get(
            "customer_invoice_transmit_method_id"
        )
        company_email = kw.get("email") or kw.get("company_email")

        # Suorita lomakkeen käsittely ensin
        res = super().address(**kw)

        # ÄLÄ kirjoita partner-tietoja jos lomakkeessa virheitä
        errors = res.qcontext.get("error")
        if errors:
            _logger.info("Skipping partner update due to errors: %s", errors)
            return res

        if kw.get("billing_address") or kw.get("checkout", {}).get("billing_address"):
            if order.partner_invoice_id:
                partner_invoice = order.with_context(
                    no_vat_validation=True
                ).partner_invoice_id
                update_values = {"type": "invoice"}

                if company_email:
                    update_values["company_email"] = company_email
                    if hasattr(partner_invoice, "email_invoicing_address"):
                        update_values["email_invoicing_address"] = company_email

                if billing_company_registry:
                    update_values["company_registry"] = billing_company_registry
                    update_values["vat"] = billing_company_registry
                    update_values["is_company"] = True
                    update_values["company_type"] = "company"

                if customer_invoice_transmit_method_id:
                    try:
                        update_values["customer_invoice_transmit_method_id"] = int(
                            customer_invoice_transmit_method_id
                        )
                    except (ValueError, TypeError):
                        _logger.warning(
                            "Invalid transmit method ID: %s",
                            customer_invoice_transmit_method_id,
                        )

                if update_values:
                    _logger.info("Writing partner_invoice values: %s", update_values)
                    partner_invoice.sudo().write(update_values)
            else:
                _logger.warning("Order does not have a partner_invoice_id!")

        elif "submitted" in kw and request.httprequest.method == "POST":
            kw["callback"] = "/shop/checkout"

        return res

    @http.route()
    def checkout(self, **post):
        res = super().checkout(**post)

        order = request.website.sale_get_order()
        if order:
            partner_invoice = order.partner_invoice_id
            if not self._check_billing_partner_mandatory_fields(partner_invoice):
                return request.redirect(
                    "/shop/address?partner_id=%d" % partner_invoice.id
                )

        return res
