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
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request

# 2. Known third party imports:
# 3. Odoo imports (openerp):

# 4. Imports from Odoo modules (rarely, and only if necessary):

# 5. Local imports in the relative form:

# 6. Unknown third party imports (One per line sorted and splitted in


class WebsiteSale(WebsiteSale):

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):

        get_param = request.env["ir.config_parameter"].sudo().get_param
        maintenance_mode = get_param("website_sale.maintenance_mode")
        company = request.env["res.company"].sudo().search([
            ('id', '=', '1')
        ])
        render_values = {"company": company}
        if maintenance_mode == "True":
            return request.render("website_sale_maintenance_mode.website_sale_template", render_values)
        else:
            response = super(WebsiteSale, self).shop(
                page=page, category=category, search=search, ppg=ppg, **post)

            return response

    @http.route()
    def product(self, product, category='', search='', **kwargs):

        get_param = request.env["ir.config_parameter"].sudo().get_param
        maintenance_mode = get_param("website_sale.maintenance_mode")
        company = request.env["res.company"].sudo().search([
            ('id', '=', '1')
        ])
        render_values = {"company": company}
        if maintenance_mode == "True":
            return request.render("website_sale_maintenance_mode.website_sale_template", render_values)
        else:
            response = super(WebsiteSale, self).product(
                product, category='', search='', **kwargs)

            return response

    @http.route()
    def pricelist_change(self, pl_id, **post):

        get_param = request.env["ir.config_parameter"].sudo().get_param
        maintenance_mode = get_param("website_sale.maintenance_mode")
        company = request.env["res.company"].sudo().search([
            ('id', '=', '1')
        ])
        render_values = {"company": company}
        if maintenance_mode == "True":
            return request.render("website_sale_maintenance_mode.website_sale_template", render_values)
        else:
            response = super(WebsiteSale, self).pricelist_change(
                pl_id, **post)

            return response

    @http.route()
    def pricelist(self, promo, **post):

        get_param = request.env["ir.config_parameter"].sudo().get_param
        maintenance_mode = get_param("website_sale.maintenance_mode")
        company = request.env["res.company"].sudo().search([
            ('id', '=', '1')
        ])
        render_values = {"company": company}
        if maintenance_mode == "True":
            return request.render("website_sale_maintenance_mode.website_sale_template", render_values)
        else:
            response = super(WebsiteSale, self).pricelist(
                promo, **post)

            return response

    @http.route()
    def cart(self, access_token=None, revive='', **post):

        get_param = request.env["ir.config_parameter"].sudo().get_param
        maintenance_mode = get_param("website_sale.maintenance_mode")
        company = request.env["res.company"].sudo().search([
            ('id', '=', '1')
        ])
        render_values = {"company": company}
        if maintenance_mode == "True":
            return request.render("website_sale_maintenance_mode.website_sale_template", render_values)
        else:
            response = super(WebsiteSale, self).cart(
                access_token=None, revive='', **post)

            return response

    @http.route()
    def address(self, **kw):

        get_param = request.env["ir.config_parameter"].sudo().get_param
        maintenance_mode = get_param("website_sale.maintenance_mode")
        company = request.env["res.company"].sudo().search([
            ('id', '=', '1')
        ])
        render_values = {"company": company}
        if maintenance_mode == "True":
            return request.render("website_sale_maintenance_mode.website_sale_template", render_values)
        else:
            response = super(WebsiteSale, self).address(
                **kw)

            return response

    @http.route()
    def checkout(self, **post):

        get_param = request.env["ir.config_parameter"].sudo().get_param
        maintenance_mode = get_param("website_sale.maintenance_mode")
        company = request.env["res.company"].sudo().search([
            ('id', '=', '1')
        ])
        render_values = {"company": company}
        if maintenance_mode == "True":
            return request.render("website_sale_maintenance_mode.website_sale_template", render_values)
        else:
            response = super(WebsiteSale, self).checkout(
                **post)

            return response

    @http.route()
    def confirm_order(self, **post):

        get_param = request.env["ir.config_parameter"].sudo().get_param
        maintenance_mode = get_param("website_sale.maintenance_mode")
        company = request.env["res.company"].sudo().search([
            ('id', '=', '1')
        ])
        render_values = {"company": company}
        if maintenance_mode == "True":
            return request.render("website_sale_maintenance_mode.website_sale_template", render_values)
        else:
            response = super(WebsiteSale, self).confirm_order(
                **post)

            return response

    @http.route()
    def extra_info(self, **post):

        get_param = request.env["ir.config_parameter"].sudo().get_param
        maintenance_mode = get_param("website_sale.maintenance_mode")
        company = request.env["res.company"].sudo().search([
            ('id', '=', '1')
        ])
        render_values = {"company": company}
        if maintenance_mode == "True":
            return request.render("website_sale_maintenance_mode.website_sale_template", render_values)
        else:
            response = super(WebsiteSale, self).extra_info(
                **post)

            return response

    @http.route()
    def payment(self, **post):

        get_param = request.env["ir.config_parameter"].sudo().get_param
        maintenance_mode = get_param("website_sale.maintenance_mode")
        company = request.env["res.company"].sudo().search([
            ('id', '=', '1')
        ])
        render_values = {"company": company}
        if maintenance_mode == "True":
            return request.render("website_sale_maintenance_mode.website_sale_template", render_values)
        else:
            response = super(WebsiteSale, self).payment(
                **post)

            return response
