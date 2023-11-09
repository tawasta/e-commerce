from odoo import http
from odoo.http import request


class CombinationInfo(http.Controller):
    @http.route("/get/more/info", type="json", auth="user", methods=["POST"])
    def get_sale_delay(self, product_id, **kw):

        current_product = (
            request.env["product.template"].sudo().search([("id", "=", product_id)])
        )

        return {"sale_delay": current_product.sale_delay}
