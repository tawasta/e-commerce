from odoo import models


class Website(models.Model):
    _inherit = "website"

    def get_pricelist_available(self, show_visible=False):
        res = super().get_pricelist_available(show_visible)

        partner = self.env.user.partner_id
        partner_pl = partner.property_product_pricelist
        public_pricelist = self.env.ref("website_sale.list_europe")

        if partner_pl and partner_pl != public_pricelist:
            # If a specific pricelist is assigned to partner, disallow using anything else
            res = partner_pl

        return res
