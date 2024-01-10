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

    def _get_alternate_languages_for_product_template(
        self, canonical_params, object_name, object_id
    ):

        """
        Function that gets called from page's <HEAD> when building the
        <link rel="alternate" hreflang="xx"/> tags for a product template
        """

        self.ensure_one()
        languages = self.language_ids

        if len(languages) <= 1:
            # no hreflang needed if no other languages
            return []

        product = request.env[object_name].sudo().browse(object_id)
        product.ensure_one()

        # Check if Canonical Link Target set for the product
        if product.website_page_canonical_link_target_id:
            # Code here is based on what is done in core's
            # website._get_alternate_languages()

            langs = []
            shorts = []

            for lg in languages:
                lg_codes = lg.code.split("_")
                short = lg_codes[0]
                shorts.append(short)
                langs.append(
                    {
                        "hreflang": ("-".join(lg_codes)).lower(),
                        "short": short,
                        "href": self._get_canonical_url_localized_for_product_template(
                            lang=lg, canonical_params=canonical_params, product=product
                        ),
                    }
                )

            # if there is only one region for a language, use only the language code
            for lang in langs:
                if shorts.count(lang["short"]) == 1:
                    lang["hreflang"] = lang["short"]

            # add the default
            langs.append(
                {
                    "hreflang": "x-default",
                    "href": self._get_canonical_url_localized_for_product_template(
                        lang=self.default_lang_id,
                        canonical_params=canonical_params,
                        product=product,
                    ),
                }
            )

            return langs

        else:
            # Fall back to core functionality
            return self._get_alternate_languages(canonical_params)
