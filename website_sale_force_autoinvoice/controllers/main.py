##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2018- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
# 2. Known third party imports:
# 3. Odoo imports (openerp):


from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale

# 4. Imports from Odoo modules (rarely, and only if necessary):

# 5. Local imports in the relative form:

# 6. Unknown third party imports (One per line sorted and splitted in


class WebsiteSale(WebsiteSale):
    @http.route()
    def shop_payment_confirmation(self, **post):
        """
        Confirm sale order and create invoice.
        """
        sale_order_id = request.session.get("sale_last_order_id")
        if sale_order_id:
            order = request.env["sale.order"].sudo().browse(sale_order_id)
            print(order)
            print(order.state)
            if order.state in ["sent", "sale"]:
                print("Creating invoices")
                if (
                    order.transaction_ids
                    and order.transaction_ids[0].provider_id.auto_create_invoice
                    == "allow"
                ):
                    order.sudo()._create_invoices()

        return super(WebsiteSale, self).shop_payment_confirmation(**post)
