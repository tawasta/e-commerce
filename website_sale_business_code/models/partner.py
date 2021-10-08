from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _commercial_fields(self):
        """ Add business id to commercial fields """
        return super()._commercial_fields() + ["business_id"]

    @api.model
    def create(self, values):
        res = super().create(values)

        # This hack can be removed when business_id is a normal char field
        # instead of relying on partner identification -module
        if res.vat and not res.business_id and res.country_id.code == "FI":
            try:
                res.business_id = "{}-{}".format(res.vat[2:9], res.vat[-1:])
            except Exception:
                # Invalid business code. Just keep the VAT
                pass

        return res
