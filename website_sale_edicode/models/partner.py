from odoo import api
from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def create_company(self):
        res = super().create_company()

        if self.parent_id:
            if not self.parent_id.edicode:
                self.parent_id.edicode = self.edicode

            if not self.parent_id.einvoice_operator:
                self.parent_id.einvoice_operator = self.einvoice_operator

        return res
