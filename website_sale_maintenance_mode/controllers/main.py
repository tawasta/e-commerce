from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    @http.route()
    def shop(self, page=0, category=None, search="", ppg=False, **post):
        company = request.env["res.company"].sudo().search([("id", "=", "1")])
        render_values = {"company": company}
        if self._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).shop(
                page=page, category=category, search=search, ppg=ppg, **post
            )

            return response

    @http.route()
    def product(self, product, category="", search="", **kwargs):
        company = request.env["res.company"].sudo().search([("id", "=", "1")])
        render_values = {"company": company}
        if self._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).product(
                product, category="", search="", **kwargs
            )

            return response

    @http.route()
    def pricelist_change(self, pricelist, **post):
        company = request.env["res.company"].sudo().search([("id", "=", "1")])
        render_values = {"company": company}
        if self._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).pricelist_change(pricelist, **post)

            return response

    @http.route()
    def pricelist(self, promo, **post):
        company = request.env["res.company"].sudo().search([("id", "=", "1")])
        render_values = {"company": company}
        if self._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).pricelist(promo, **post)

            return response

    @http.route()
    def cart(self, access_token=None, revive="", **post):
        company = request.env["res.company"].sudo().search([("id", "=", "1")])
        render_values = {"company": company}
        if self._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).cart(
                access_token=None, revive="", **post
            )

            return response

    @http.route()
    def address(self, **kw):
        company = request.env["res.company"].sudo().search([("id", "=", "1")])
        render_values = {"company": company}
        if self._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).address(**kw)

            return response

    @http.route()
    def checkout(self, **post):
        company = request.env["res.company"].sudo().search([("id", "=", "1")])
        render_values = {"company": company}
        if self._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).checkout(**post)

            return response

    @http.route()
    def confirm_order(self, **post):
        company = request.env["res.company"].sudo().search([("id", "=", "1")])
        render_values = {"company": company}
        if self._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).confirm_order(**post)

            return response

    @http.route()
    def extra_info(self, **post):
        company = request.env["res.company"].sudo().search([("id", "=", "1")])
        render_values = {"company": company}
        if self._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).extra_info(**post)

            return response

    @http.route()
    def payment(self, **post):
        company = request.env["res.company"].sudo().search([("id", "=", "1")])
        render_values = {"company": company}
        if self._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).payment(**post)

            return response

    def _maintenance_mode(self):
        # If maintenance mode is set, and user doesn't belong to website editors
        get_param = request.env["ir.config_parameter"].sudo().get_param
        maintenance_mode = get_param("website_sale.maintenance_mode")

        return maintenance_mode == "True" and not request.env.user.has_group(
            "website.group_website_designer"
        )
