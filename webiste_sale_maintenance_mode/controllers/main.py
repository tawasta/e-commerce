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
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

# 2. Known third party imports:
# 3. Odoo imports (openerp):

# 4. Imports from Odoo modules (rarely, and only if necessary):

# 5. Local imports in the relative form:

# 6. Unknown third party imports (One per line sorted and splitted in


class WebsiteSale(WebsiteSale):

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):

        get_param = request.env["ir.config_parameter"].sudo().get_param
        maintenance_mode = get_param("website_sale.maintenance_mode")
        company = request.env["res.company"].sudo().search([
            ('id', '=', '1')
        ])
        render_values = {"company": company}

        if maintenance_mode == "True":
            return request.render("webiste_sale_maintenance_mode.website_sale_template", render_values)
        else:
            response = super(WebsiteSale, self).shop(
                page=page, category=category, search=search, ppg=ppg, **post)

            return response
