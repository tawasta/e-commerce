from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def _get_mandatory_billing_fields(self):
        # deprecated for _get_mandatory_fields_billing which handle zip/state required
        return [
            "name",
            "email",
            "street",
            "city",
            "country_id",
            "firstname",
            "lastname",
        ]

    def _get_mandatory_shipping_fields(self):
        # deprecated for _get_mandatory_fields_shipping which handle zip/state required
        return ["name", "street", "city", "country_id", "firstname", "lastname"]

    @http.route()
    def address(self, **kw):
        if "submitted" in kw and kw.get("firstname"):
            name = request.env["res.partner"]._get_computed_name(
                kw.get("lastname"), kw.get("firstname")
            )
            kw["name"] = name
            response = super().address(**kw)
        else:
            response = super().address(**kw)

        # Read the address mode core already computed instead of the
        # request's raw query string: a plain form POST doesn't repeat the
        # URL's query string, so "mode=billing" is lost from
        # request.httprequest.args as soon as a validation error re-renders
        # the page after submission.
        is_billing_mode = "billing" in (response.qcontext.get("mode") or ())

        # Välitetään is_billing_mode templateen
        response.qcontext.update(
            {
                "is_billing_mode": is_billing_mode,
            }
        )

        return response
