from odoo import http
from odoo.http import request

from odoo.addons.website_sale_split_name.controllers.main import WebsiteSale


class CustomWebsiteSale(WebsiteSale):
    @http.route()
    def address(self, **kw):
        if "submitted" in kw:
            if "name" in kw and kw.get("name"):
                kw["name"] = kw.get("name")
                #name_parts = kw.get("name").split(" ", 1)
                # if len(name_parts) == 2:
                #     firstname, lastname = name_parts
                #     kw["firstname"] = firstname
                #     kw["lastname"] = lastname
                # else:
                #     kw["firstname"] = " "
                #     kw["lastname"] = kw.get("name")
            else:
                name = request.env["res.partner"]._get_computed_name(
                    kw.get("lastname"), kw.get("firstname")
                )
                kw["name"] = name

        return super(CustomWebsiteSale, self).address(**kw)
