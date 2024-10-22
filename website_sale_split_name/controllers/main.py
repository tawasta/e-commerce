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
        # Tarkistetaan, onko URL:ssa parametri mode=billing, tai "billing_address" jo parametreissa
        is_billing_mode = request.httprequest.args.get("mode") == "billing" or kw.get(
            "billing_address", {}
        )

        if "submitted" in kw and kw.get("firstname"):
            name = request.env["res.partner"]._get_computed_name(
                kw.get("lastname"), kw.get("firstname")
            )
            kw["name"] = name
            response = super(WebsiteSale, self).address(**kw)
        else:
            response = super(WebsiteSale, self).address(**kw)

        # Välitetään is_billing_mode templateen
        response.qcontext.update(
            {
                "is_billing_mode": is_billing_mode,
            }
        )

        return response
