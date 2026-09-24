import logging

from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):
    def _checkout_form_save(self, mode, checkout, all_values):
        # Add company registry to saved values if one was provided instead of VAT

        vat_field_input = all_values.get("vat", False)
        country_input = all_values.get("country_id", False)

        is_finland = (
            country_input and int(country_input) == request.env.ref("base.fi").id
        )

        if is_finland and vat_field_input:
            checkout["company_registry"] = all_values["vat"]
            checkout.pop("vat", False)

        return super()._checkout_form_save(mode, checkout, all_values)

    def checkout_form_validate(self, mode, all_form_values, data):
        # Validate the Company Registry / VAT field
        # - If country is Finland, assume format to be 1234567-1
        # - For other countries, use the standard VAT validation functionality of core

        # in website_sale_billing_address, when reaching address page with mode=billing
        # the name of the form field is "billing_company_registry" instead of "vat".
        # Handle both cases

        vat_field_filled = "vat" in data
        billing_company_registry_filled = "billing_company_registry" in data

        if vat_field_filled:
            vat_field_input = data.get("vat", False)
        elif billing_company_registry_filled:
            vat_field_input = data.get("billing_company_registry", False)
        else:
            vat_field_input = False

        country_input = data.get("country_id", False)

        is_finland = (
            country_input and int(country_input) == request.env.ref("base.fi").id
        )

        # Pop the Y-tunnus value so it doesn't get validated as a VAT code
        if is_finland and vat_field_input:
            if vat_field_filled:
                data.pop("vat")
            elif billing_company_registry_filled:
                data.pop("billing_company_registry")

        # Run all the standard validations
        error, error_message = super().checkout_form_validate(
            mode, all_form_values, data
        )

        # Apply finnish company registry y-tunnus validation on top
        if is_finland and vat_field_input:
            try:
                partner_dummy = request.env["res.partner"].new(
                    {
                        "company_registry": vat_field_input,
                        "country_id": int(country_input),
                    }
                )

                partner_dummy.sudo()._company_registry_validate_fi()

            except ValidationError as exception:
                # Human-readable validation message is
                # provided by l10n_fi_company_registry
                if vat_field_filled:
                    error["vat"] = "error"
                elif billing_company_registry_filled:
                    error["billing_company_registry"] = "error"

                error_message.append(exception.args[0])

            finally:
                # Put the popped value back, also when the validation failed,
                # so that overrides running after this one still see it
                if vat_field_filled:
                    data["vat"] = vat_field_input
                elif billing_company_registry_filled:
                    data["billing_company_registry"] = vat_field_input

        return error, error_message
