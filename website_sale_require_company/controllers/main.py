import logging
from odoo import _
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.tools import is_html_empty


_logger = logging.getLogger(__name__)


class WebsiteSaleRequireCompany(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super()._get_shop_payment_values(order, **kwargs)

        requires_company_info = True in order.order_line.mapped(
            "product_id.requires_company_info"
        )

        has_company_info = order.partner_id.parent_id or order.partner_id.vat

        if requires_company_info and not has_company_info:
            # Order requires company info, but doesn't have any
            values["errors"].append(
                (
                    _("You will need to provide company information"),
                    _("Please return to address step and add invoicing details"),
                )
            )

        return values
