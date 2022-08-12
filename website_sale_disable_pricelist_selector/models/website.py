from odoo import models


class Website(models.Model):
    _inherit = "website"

    def _get_pricelist_available(self, req, show_visible=False):
        res = super()._get_pricelist_available(req, show_visible)

        partner = self.env.user.partner_id
        partner_pl = partner.property_product_pricelist
        public_pricelist = self.env.ref("product.list0")

        if partner_pl and partner_pl != public_pricelist:
            # If a specific pricelist is assigned to partner, disallow using anything else
            res = partner_pl

        return res
