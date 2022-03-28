##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:
import logging

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import http, _
from odoo.http import request

# 4. Imports from Odoo modules:
from odoo.addons.website_sale.controllers.main import WebsiteSale

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class WebsiteSaleRecaptcha(WebsiteSale):
    @http.route(
        ["/shop/cart/update"],
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
        csrf=False,
    )
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        if not kw.get("g-recaptcha-response"):
            _logger.warn(
                _(
                    "Adding product %s to shopping cart denied. No Google Recaptcha Response for user %s."
                    % (product_id, request.env.user)
                )
            )
            return request.render("website.404")
        res = super(WebsiteSaleRecaptcha, self).cart_update(
            product_id, add_qty=1, set_qty=0, **kw
        )
        return res
