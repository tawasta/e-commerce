import logging
from odoo import _
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSaleRequireAttachment(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super()._get_shop_payment_values(order, **kwargs)

        requires_attachment = True in order.order_line.mapped(
            "product_id.requires_attachment"
        )
        # We could check if the number of needed attachments match given attachments here
        has_attachment = order.message_attachment_count > 0

        if requires_attachment and not has_attachment:
            # Order requires an attachment, but doesn't have one
            lines = order.order_line.filtered(
                lambda l: l.product_id.requires_attachment
            )
            errors = []
            for line in lines:
                product = line.product_id
                explanation = product.requires_attachment_help or _(
                    "Needs attachment"
                )

                errors.append(_("%s: %s", product.name, explanation))

            error_text = ", ".join(errors)

            values["errors"].append(
                (
                    _("Please return to the previous step and add an attachment"),
                    error_text,
                )
            )

        return values
