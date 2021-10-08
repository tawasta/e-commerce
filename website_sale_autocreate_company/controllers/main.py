from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def _checkout_form_save(self, mode, checkout, all_values):
        """
        Auto-create a company if company name is set
        """

        res = super(WebsiteSale, self)._checkout_form_save(mode, checkout, all_values)

        if checkout.get("company_name"):
            partner = request.env["res.partner"].sudo().browse([res])
            if partner:
                partner.create_company()

        return res
