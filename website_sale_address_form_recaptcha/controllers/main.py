import logging

from odoo import _, http
from odoo.exceptions import UserError
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale as WebsiteSaleOriginal

_logger = logging.getLogger(__name__)


class WebsiteSaleAddressRecaptcha(WebsiteSaleOriginal):
    @http.route()
    def address(self, **post):
        if "submitted" in post and request.httprequest.method == "POST":
            if not request.env["ir.http"]._verify_request_recaptcha_token(
                "website_sale_address_form"
            ):
                raise UserError(_("Suspicious activity detected by Google reCaptcha."))

        return super().address(**post)
