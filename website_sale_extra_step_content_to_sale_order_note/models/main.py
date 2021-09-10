from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSaleForm


class ExtraStepNote(WebsiteSaleForm):
    @http.route()
    def website_form_saleorder(self, **kwargs):
        order = http.request.website.sale_get_order()

        if kwargs.get("Give us your feedback"):
            if kwargs.get("Give us your feedback"):
                order.note = kwargs.get("Give us your feedback")

        return super(ExtraStepNote, self).website_form_saleorder(**kwargs)
