import logging

from odoo import models
from odoo.http import request

_logger = logging.getLogger(__name__)


class Website(models.Model):

    _inherit = "website"

    def _get_canonical_url_localized_for_product_template(
        self, lang, canonical_params, product
    ):
        """
        Returns an url, e.g.
        http://my-odoo-installation.com/fi/example-target-page, based on the
        product's "Canonical Link Target" field
        """

        # At this point we know website_page_canonical_link_target_id is set
        page_properties = (
            product.sudo().website_page_canonical_link_target_id.get_page_properties()
        )
        page_url = page_properties["url"]

        lang_path = ("/" + lang.url_code) if lang != self.default_lang_id else ""
        localized_path = lang_path + page_url

        return self.get_base_url() + localized_path

    def _get_canonical_url_for_product_template(
        self, canonical_params, object_name, object_id
    ):
        """
        Function that gets called from page's <HEAD> when building the
        <link rel="canonical"/> tag for a product template
        """

        product = request.env[object_name].sudo().browse(object_id)
        product.ensure_one()

        # Check if Canonical Link Target set for the product
        if product.website_page_canonical_link_target_id:
            # Call custom url building functionality
            return self._get_canonical_url_localized_for_product_template(
                lang=request.lang, canonical_params=canonical_params, product=product
            )
        else:
            # Fall back to core functionality that handles also the localization
            return self._get_canonical_url(canonical_params)
