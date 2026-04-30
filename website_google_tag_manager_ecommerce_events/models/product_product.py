import json
import logging

from markupsafe import Markup

from odoo import models

_logger = logging.getLogger(__name__)


def _ga4_safe_json(payload):
    """Serialize a payload for inline <script>, escaping </ to prevent
    early script tag termination if a product name contains it."""
    return json.dumps(payload).replace("</", "<\\/")


def _ga4_push_script(payload):
    """Build a Markup-wrapped <script> body that resets the ecommerce
    object and pushes the given GA4 event payload to dataLayer."""

    body = (
        "window.dataLayer=window.dataLayer||[];"
        "window.dataLayer.push({ecommerce:null});"
        "window.dataLayer.push(%s);" % _ga4_safe_json(payload)
    )
    return Markup(body)


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _ga4_item(self, quantity=1.0, price=None):
        """Return one entry of GA4's `items` array for this variant."""

        self.ensure_one()
        return {
            "item_id": self.default_code or str(self.id),
            "item_name": self.display_name,
            "item_category": self.categ_id.name or "",
            "price": price if price is not None else self.lst_price,
            "quantity": quantity,
        }

    def _ga4_view_item_script(self):
        """Build the view_item dataLayer push for the product page."""
        self.ensure_one()

        website = self.env["website"].get_current_website()
        currency = website.currency_id.name
        payload = {
            "event": "view_item",
            "ecommerce": {
                "currency": currency,
                "value": self.lst_price,
                "items": [self._ga4_item()],
            },
        }
        return _ga4_push_script(payload)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _ga4_view_item_script(self):
        """Convenience wrapper so templates can call it on product.template."""

        self.ensure_one()
        variant = self.product_variant_id
        if not variant:
            return Markup("")
        return variant._ga4_view_item_script()
