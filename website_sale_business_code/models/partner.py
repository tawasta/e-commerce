from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _commercial_fields(self):
        """ Add business id to commercial fields """
        return super()._commercial_fields() + ["business_code"]
