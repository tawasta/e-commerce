from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def create_company(self):
        res = super().create_company()

        if self.parent_id:
            if not self.parent_id.email:
                self.parent_id.email = self.email

        return res
