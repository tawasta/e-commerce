import logging
from odoo import _
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request

_logger = logging.getLogger(__name__)


class WebsiteSaleRequireAttachment(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super()._get_shop_payment_values(order, **kwargs)

        if (
            request.website.checkout_pay_now_button_label
            and len(request.website.checkout_pay_now_button_label.strip()) > 0
        ):
            values[
                "submit_button_label"
            ] = request.website.checkout_pay_now_button_label

        return values
