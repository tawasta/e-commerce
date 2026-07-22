from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.website import WebsiteSaleForm


class ExtraStepNote(WebsiteSaleForm):
    @http.route()
    def website_form_saleorder(self, **kwargs):
        if kwargs.get("Give us your feedback"):
            request.cart.customer_feedback = kwargs.get("Give us your feedback")

        return super().website_form_saleorder(**kwargs)
