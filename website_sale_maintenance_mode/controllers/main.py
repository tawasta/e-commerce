from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleMaintenance(WebsiteSale):
    @http.route()
    def shop(self, page=0, category=None, search="", ppg=False, **post):
        render_values = {"company": request.website.company_id}
        if request.website._maintenance_mode():
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
        render_values = {"company": request.website.company_id}
        if request.website._maintenance_mode():
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
        render_values = {"company": request.website.company_id}
        if request.website._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).pricelist_change(pricelist, **post)

            return response

    @http.route()
    def pricelist(self, promo, **post):
        render_values = {"company": request.website.company_id}
        if request.website._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).pricelist(promo, **post)

            return response

    @http.route()
    def cart(self, access_token=None, revive="", **post):
        render_values = {"company": request.website.company_id}
        if request.website._maintenance_mode():
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
        render_values = {"company": request.website.company_id}
        if request.website._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).address(**kw)

            return response

    @http.route()
    def checkout(self, **post):
        render_values = {"company": request.website.company_id}
        if request.website._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).checkout(**post)

            return response

    @http.route()
    def confirm_order(self, **post):
        render_values = {"company": request.website.company_id}
        if request.website._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).confirm_order(**post)

            return response

    @http.route()
    def extra_info(self, **post):
        render_values = {"company": request.website.company_id}
        if request.website._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).extra_info(**post)

            return response

    @http.route()
    def payment(self, **post):
        render_values = {"company": request.website.company_id}
        if request.website._maintenance_mode():
            return request.render(
                "website_sale_maintenance_mode.website_sale_template", render_values
            )
        else:
            response = super(WebsiteSale, self).payment(**post)

            return response
