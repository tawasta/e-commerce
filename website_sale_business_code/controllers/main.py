import re

from odoo import _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def _checkout_form_save(self, mode, checkout, all_values):
        """
        Add edicode and operator to saved values
        """
        vat = checkout.get("vat")
        country_id = checkout.get("country_id")

        if country_id and vat and vat[0].isdigit():
            # Change VAT-field format to correct vat-format
            # Parse everything else except numbers and add country code in front
            country_code = (
                request.env["res.country"].search([("id", "=", country_id)]).code
            )

            checkout["vat"] = country_code + re.sub("[^0-9]", "", checkout["vat"])

        print(checkout)

        res = super(WebsiteSale, self)._checkout_form_save(mode, checkout, all_values)

        return res

    def checkout_form_validate(self, mode, all_form_values, data):
        """
        Change vat to correct format to accept business id format
        """
        fi_code = request.env.ref("base.fi").code
        vat = data.get("vat")
        country_code = False

        if vat and data.get("country_id"):
            country_code = (
                request.env["res.country"]
                .search([("id", "=", data.get("country_id"))])
                .code
            )
            data["vat"] = country_code + re.sub("[^0-9]", "", data["vat"])

        res = super(WebsiteSale, self).checkout_form_validate(
            mode, all_form_values, data
        )

        if vat and country_code == fi_code:
            # Change back to original format to avoid end user confusion
            data["vat"] = vat

        return res
