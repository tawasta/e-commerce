from odoo import http
from odoo.http import request
import logging
from odoo import fields, http, SUPERUSER_ID, tools, _
from werkzeug.exceptions import Forbidden, NotFound
from odoo.exceptions import ValidationError
from odoo.osv import expression

from odoo.addons.website_sale_split_name.controllers.main import WebsiteSale


class CustomWebsiteSale(WebsiteSale):


    def _get_mandatory_shipping_fields(self):
        # Remove 'firstname' and 'lastname' from mandatory fields for shipping
        fields = super(CustomWebsiteSale, self)._get_mandatory_shipping_fields()
        fields.remove('firstname')
        fields.remove('lastname')
        return fields

    @http.route()
    def address(self, **kw):
        logging.info(kw);
        if "submitted" in kw:
            if "name" in kw and kw.get("name"):
                kw["name"] = kw.get("name")
            else:
                name = request.env["res.partner"]._get_computed_name(
                    kw.get("lastname"), kw.get("firstname")
                )
                kw["name"] = name

        return super(CustomWebsiteSale, self).address(**kw)
