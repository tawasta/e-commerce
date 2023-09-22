from odoo import http, _
from odoo.http import request
import logging
import json

class WebsiteSaleTracking(http.Controller):
    @http.route(
        [
            "/my/add_product_tracking",
        ],
        type="json",
        auth="user",
        website=True,
    )
    def add_product_tracking(
        self, email=None, product_id=None, **kw
    ):
        res = {}
        res["msg"] = _("Product successfully added to tracking!")
        logging.info("=======TAAAAAALLAAAAAA========");
        if product_id and email:
            partner = request.env.user.partner_id
            product = request.env['product.product'].sudo().browse(int(product_id))
            tracking_values = {
                'product_id': product.id,
                'email': email,
            }
            logging.info("==========MENENENENE========");
            request.env['product.tracking'].sudo().create(tracking_values)
        return json.dumps(res)
