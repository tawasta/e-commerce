from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    @http.route(
        "/shop/address/submit",
        type="http",
        methods=["POST"],
        auth="public",
        website=True,
        sitemap=False,
    )
    def shop_address_submit(
        self,
        partner_id=None,
        address_type="billing",
        use_delivery_as_billing=None,
        callback=None,
        **form_data,
    ):
        res = super().shop_address_submit(
            partner_id, address_type, use_delivery_as_billing, callback, **form_data
        )
        if form_data.get("company_name"):
            partner_sudo, address_type = self._prepare_address_update(
                http.request.cart,
                partner_id=partner_id and int(partner_id),
                address_type=address_type,
            )
            if partner_sudo:
                partner_sudo.create_company()
        return res
