from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    @http.route()
    def address(self, **kw):
        if "submitted" in kw:
            response = super(WebsiteSale, self).address(**kw)
            is_sale_privacies = request.env["privacy.activity"].sudo().search([
                ("default_in_website_sale", "=", "True")
            ])
            if is_sale_privacies:
                order = request.website.sale_get_order()
                self._create_privacy(kw, order.partner_id)
        else:
            response = super(WebsiteSale, self).address(**kw)

        return response

    def _create_privacy(self, kw, partner):
        """ Create privacies """
        privacy_ids = []
        sale_privacies = request.env["privacy.activity"].sudo().search([
            ("default_in_website_sale", "=", "True")
        ])
        for privacy in sale_privacies:
            if kw.get("privacy_" + str(privacy.id)):
                privacy_ids.append(privacy.id)

        for pr in sale_privacies:
            accepted = pr.id in privacy_ids
            privacy_values = {
                "partner_id": partner.id,
                "activity_id": pr.id,
                "accepted": accepted,
                "state": "answered",
            }
            already_privacy_record = (
                request.env["privacy.consent"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", partner.id,),
                        ("activity_id", "=", pr.id),
                    ]
                )
            )
            if already_privacy_record:
                already_privacy_record.sudo().write({"accepted": accepted})
            else:
                request.env["privacy.consent"].sudo().create(privacy_values)
