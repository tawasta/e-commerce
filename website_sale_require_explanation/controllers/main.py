import logging
from odoo import _
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.tools import is_html_empty


_logger = logging.getLogger(__name__)


class WebsiteSaleRequireExplanation(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super()._get_shop_payment_values(order, **kwargs)

        requires_explanation = True in order.order_line.mapped(
            "product_id.requires_explanation"
        )

        no_explanation = is_html_empty(order.note)
        if no_explanation and hasattr(order, "description"):
            # Also accept explanation in the "description"-field
            no_explanation = is_html_empty(order.note)

        if requires_explanation and no_explanation:
            # Order requires an explanation, but doesn't have one
            lines = order.order_line.filtered(
                lambda l: l.product_id.requires_explanation
            )
            errors = []
            for line in lines:
                product = line.product_id
                explanation = product.requires_explanation_help or _(
                    "Needs explanation"
                )

                errors.append(_("%s: %s", product.name, explanation))

            error_text = ", ".join(errors)

            values["errors"].append(
                (
                    _("Please return to the previous step and add an explanation"),
                    error_text,
                )
            )

        return values
