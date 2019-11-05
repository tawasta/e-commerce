
# 1. Standard library imports:
from datetime import datetime
from dateutil import parser

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import http, _
from odoo.http import request

# 4. Imports from Odoo modules:
from odoo.addons.website_sale.controllers.main import WebsiteSale

# 5. Local imports in the relative form:

# 6. Unknown third party imports


class WebsiteSaleCoupon(WebsiteSale):

    @http.route(
        ['/shop/coupon/use'],
        type='json',
        auth='public',
        website=True)
    def coupon_use(self, **post):
        # JSON-route for redeeming coupons

        coupon = request.env['website.sale.coupon'].sudo().search([
            ('code', '=', post.get('code', False))
        ], limit=1)

        res = dict()

        # Validation errors.
        # Each conditionals purpose should be explained in the error-message
        if not coupon:
            res['error'] = _("Coupon doesn\'t exist!")
        elif coupon.available == 0:
            res['error'] = _("This coupon has already been used")
        elif coupon.start_date and \
                parser.parse(coupon.start_date) > datetime.now():
            res['error'] = _("This coupon isn\'t active yet")
        elif coupon.end_date and \
                parser.parse(coupon.end_date) < datetime.now():
            res['error'] = _("This coupon has expired")
        elif coupon.partner_id and request.env.uid != coupon.partner_id.id:
            res['error'] = _("This coupon isn't yours")

        # Coupon is fine. Try to use it
        if 'error' not in res:
            coupon_used = request.website.sale_get_order(force_create=1)\
                ._use_coupon(coupon)
            if coupon_used:
                res['error'] = coupon_used

        return res

    @http.route(
        ['/shop/coupon/remove'],
        type='json',
        auth='public',
        website=True)
    def coupon_remove(self, **post):
        # JSON-route for removing coupons from SO lines

        # Remove the coupon log entry and replenish the coupon availability
        if post.get('coupon_id', False):
            sale_order = request.website.sale_get_order()

            coupon_log = request.env['website.sale.coupon.log'].sudo().search([
                ('coupon_id.id', '=', post.get('coupon_id')),
                ('sale_order_id', '=', sale_order.id),
            ])

            if coupon_log:
                if coupon_log.coupon_id.available >= 0:
                    coupon_log.coupon_id.available += 1
                coupon_log.active = False
