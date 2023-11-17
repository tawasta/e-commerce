from odoo.http import request
from odoo.osv import expression

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super(WebsiteSale, self)._get_shop_payment_values(order, **kwargs)

        groups_ids = request.env.user.groups_id

        domain = expression.AND(
            [
                [
                    ("state", "in", ["enabled", "test"]),
                ],
                [
                    "|",
                    ("website_id", "=", False),
                    ("website_id", "=", request.website.id),
                ],
                [
                    "|",
                    ("country_ids", "=", False),
                    ("country_ids", "in", [order.partner_id.country_id.id]),
                ],
                [
                    "|",
                    ("allowed_group_ids", "=", False),
                    ("allowed_group_ids", "in", groups_ids.ids),
                ],
            ]
        )

        acquirers = request.env["payment.acquirer"].search(domain)
        values["acquirers"] = acquirers
        return values
