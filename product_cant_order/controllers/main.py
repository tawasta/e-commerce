from odoo import http
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
        try:
            product = (
                request.env["product.product"]
                .sudo()
                .search([("id", "=", product_id)], limit=1)
            )
            if product:
                values = {"can_not_order": product.can_not_order}
            else:
                values = {"error": "Product not found"}

        except Exception as e:
            values = {"error": str(e)}

        return values
