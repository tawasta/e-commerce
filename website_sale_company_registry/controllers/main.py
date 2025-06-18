import re

from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.exceptions import ValidationError

import logging

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

        vat_field_input = data.get("vat", False)
        country_input = data.get("country_id", False)

        is_finland = (
            country_input and int(country_input) == request.env.ref("base.fi").id
        )

        # Pop the Y-tunnus value so it doesn't get validated as a VAT code
        if is_finland and vat_field_input:
            data.pop("vat")

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

                data["vat"] = vat_field_input
            except ValidationError as exception:
                # Human-readable validation message is
                # provided by l10n_fi_company_registry
                error["vat"] = "error"
                error_message.append(exception.args[0])

        return error, error_message
