from odoo import http, exceptions, _
from odoo.http import request


class CheckProduct(http.Controller):
    @http.route(
        ["/check/product/<int:product_id>"],
        type="json",
        auth="public",
        website=True,
        csrf=False,
    )
    def get_product(self, product_id=None, **post):
        """
        Checks if the provided variant ID can be added to cart.
        """

        product = (
            request.env["product.product"]
            .sudo()
            .search([("id", "=", product_id)], limit=1)
        )
        if product:
            return {"can_not_order": product.can_not_order}
        else:
            raise exceptions.ValidationError(_("Product ID %s not found", product_id))
