from odoo import _
from odoo.http import request

from odoo.addons.phone_validation.tools.phone_validation import phone_format
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleAddressPhoneCountryCode(WebsiteSale):
    def _phone_country_from_post(self, values):
        """Map the posted phone country code to a res.country, empty if unknown."""
        # sudo: public checkout visitors must resolve their own posted code
        Country = request.env["res.country"].sudo()
        code = str(values.get("phone_country_code") or "").strip().upper()
        return (
            Country.search([("code", "=", code)], limit=1) if code else Country.browse()
        )

    def checkout_form_validate(self, mode, all_form_values, data):
        """Require a valid country code whenever a phone number is given."""

        error, error_message = super().checkout_form_validate(
            mode, all_form_values, data
        )
        if data.get("phone") and not self._phone_country_from_post(data):
            error["phone_country_code"] = "missing"
            error_message.append(_("Please select a phone country code."))
        return error, error_message

    def values_postprocess(self, order, mode, values, errors, error_msg):
        """Normalize the phone number to E.164 via libphonenumber."""

        new_values, errors, error_msg = super().values_postprocess(
            order, mode, values, errors, error_msg
        )
        phone = new_values.get("phone")
        country = self._phone_country_from_post(values) if phone else False
        if country and country.code and country.phone_code:
            new_values["phone"] = phone_format(
                phone,
                country.code,
                country.phone_code,
                force_format="E164",
                raise_exception=False,
            )
        return new_values, errors, error_msg
