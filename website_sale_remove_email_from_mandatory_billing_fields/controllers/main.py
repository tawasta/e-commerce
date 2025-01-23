from odoo.addons.website_sale.controllers.main import WebsiteSale

import logging

_logger = logging.getLogger(__name__)


class WebsiteSaleBilling(WebsiteSale):
    def _get_mandatory_fields_billing(self, country_id=False):
        """Remove email from mandatory fields"""
        res = super()._get_mandatory_fields_billing(country_id)

        if "email" in res:
            res.remove("email")

        return res
