import logging
from odoo import _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


_logger = logging.getLogger(__name__)


class WebsiteSaleRequireCompany(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super()._get_shop_payment_values(order, **kwargs)

        required_category_ids = order.order_line.mapped(
            "product_id.required_product_category_id"
        )

        existing_category_ids = order.order_line.mapped("product_id.public_categ_ids")

        missing_category_ids = [
            x for x in required_category_ids.ids if x not in existing_category_ids.ids
        ]

        if missing_category_ids:
            # Order a product from certain category, but doesn't have one
            missing_categories = (
                request.env["product.public.category"]
                .sudo()
                .browse(missing_category_ids)
            )
            missing_category_names = ", ".join(missing_categories.mapped("name"))

            values["missing_category_ids"] = missing_categories
            values["errors"].append(
                (
                    _("You are required to add a product to your order"),
                    _(
                        "Please add product from following categories: %s",
                        missing_category_names,
                    ),
                )
            )

        return values
