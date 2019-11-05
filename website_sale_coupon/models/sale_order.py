
# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import models, _

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def _use_coupon(self, coupon):
        # Use coupon. Checks all SO lines for applicability
        # Returns False if there are no errors
        error = False

        if not coupon:
            error = _("No code provided")

        coupon_used = False
        for order_line in self.order_line:
            if order_line._use_coupon(coupon):
                coupon_used = True

                if coupon.type == 'fixed':
                    # Only add the fixed coupon once
                    break

        if not coupon_used:
            error = _("This coupon is already in use or doesn't \
                      match any products in your cart.")

        if coupon_used and coupon.available > 0:
            coupon.available -= 1

        return error
