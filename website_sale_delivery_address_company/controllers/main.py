from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    def _checkout_form_save(self, mode, checkout, all_values):
        partner_id = super(WebsiteSale, self)._checkout_form_save(
            mode, checkout, all_values
        )

        # Overwrite the partner type
        if mode[0] == 'new':
            res_partner = request.env['res.partner']
            res_partner.sudo().browse([partner_id]).is_company = True

        return partner_id
