import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ProductPricelist(models.Model):

    _inherit = "product.pricelist"

    def _get_website_pricelists_domain(self, website_id):

        if self._context.get("exclude_website_sale_pricelist_domain"):
            _logger.debug(
                "_get_website_pricelists_domain: Bypassing "
                "website_sale pricelist domain."
            )
            return []
        else:
            return super()._get_website_pricelists_domain(website_id)

    def _get_partner_pricelist_multi_filter_hook(self):

        if self._context.get("exclude_website_sale_pricelist_domain"):
            _logger.debug(
                "_get_partner_pricelist_multi_filter_hook: "
                "Bypassing website_sale pricelist domain."
            )
            # Use the logic of core when there is no website_sale installed
            return self.filtered("active")
        else:
            return super()._get_partner_pricelist_multi_filter_hook()
