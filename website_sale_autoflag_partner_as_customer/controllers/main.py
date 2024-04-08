from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def _checkout_form_save(self, mode, checkout, all_values):
        """
        Autoset the is_customer field provided by oca's partner_manual_rank module
        """

        res = super(WebsiteSale, self)._checkout_form_save(mode, checkout, all_values)

        partner = request.env["res.partner"].sudo().browse([res])
        partner.sudo().write({"is_customer": True})

        return res
