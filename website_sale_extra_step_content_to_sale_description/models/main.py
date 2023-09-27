from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSaleForm


class ExtraStepNote(WebsiteSaleForm):
    @http.route()
    def website_form_saleorder(self, **kwargs):
        order = http.request.website.sale_get_order()

        if kwargs.get("description"):
            order.description = kwargs.get("description")

        return super(ExtraStepNote, self).website_form_saleorder(**kwargs)
