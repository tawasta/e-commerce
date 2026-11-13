from odoo import _
from odoo.exceptions import UserError
from odoo.http import request

from odoo.addons.phone_validation.tools.phone_validation import (
    phone_format,
    phone_get_country_code_for_number,
    phone_parse,
)
from odoo.addons.website_sale.controllers.main import WebsiteSale

# A lone dash is used as a placeholder for "no phone" so that core's required
# check passes; it is not a number to validate.
NO_PHONE_PLACEHOLDER = "-"


class WebsiteSaleAddressPhoneCountryCode(WebsiteSale):
    def _is_phone_given(self, phone):
        # Blank counts as missing, like core's required field check
        phone = (phone or "").strip()
        return bool(phone) and phone != NO_PHONE_PLACEHOLDER

    def _phone_country_from_post(self, values):
        """Return the posted phone country, empty if unknown or without a
        dialing code."""
        Country = request.env["res.country"]
        country_id = str(values.get("phone_country_id") or "")
        # isdecimal, not isdigit: int() rejects digits like "²"
        if not country_id.isdecimal():
            return Country
        return Country.browse(int(country_id)).exists().filtered("phone_code")

    def _phone_country_from_number(self, phone):
        """Return the country of an international number, empty otherwise."""
        Country = request.env["res.country"]
        code = phone_get_country_code_for_number(phone) if phone else ""
        return Country.search([("code", "=", code)], limit=1) if code else Country

    def _get_country_related_render_values(self, kw, render_values):
        """Add the phone country preselected in the address form."""
        values = super()._get_country_related_render_values(kw, render_values)
        checkout = render_values["checkout"]
        # A posted form keeps the customer's own choice, even an empty one
        if "phone_country_id" in checkout:
            values["phone_country_selected"] = str(checkout["phone_country_id"] or "")
            return values

        phone = checkout["phone"] if "phone" in checkout else False
        # The number's country only if the dropdown offers it (in shipping
        # mode core limits countries to the delivery countries)
        number_country = self._phone_country_from_number(phone) & values["countries"]
        country = number_country or values["country"]
        values["phone_country_selected"] = str(country.id) if country else ""
        return values

    def checkout_form_validate(self, mode, all_form_values, data):
        """Require a phone country and a valid number whenever a phone is
        given."""

        error, error_message = super().checkout_form_validate(
            mode, all_form_values, data
        )
        phone = data.get("phone")
        if not self._is_phone_given(phone):
            return error, error_message

        country = self._phone_country_from_post(data)
        if not country:
            error["phone_country_id"] = "missing"
            error_message.append(_("Please select a phone country code."))
            return error, error_message

        # Same parser as phone_format in values_postprocess, so a number that
        # passes here is always stored in E.164.
        try:
            phone_parse(phone, country.code)
        except UserError:
            error["phone"] = "error"
            error_message.append(_("Please enter a valid phone number."))
        return error, error_message

    def values_postprocess(self, order, mode, values, errors, error_msg):
        """Normalize the phone number to E.164 via libphonenumber."""

        new_values, errors, error_msg = super().values_postprocess(
            order, mode, values, errors, error_msg
        )
        phone = new_values.get("phone")
        if not self._is_phone_given(phone):
            return new_values, errors, error_msg

        country = self._phone_country_from_post(values)
        if country:
            # Core runs this also when validation failed: an invalid number
            # must not raise here, the form already shows the error.
            new_values["phone"] = phone_format(
                phone,
                country.code,
                country.phone_code,
                force_format="E164",
                raise_exception=False,
            )
        return new_values, errors, error_msg
