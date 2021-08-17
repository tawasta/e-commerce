from odoo import api
from odoo import fields
from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    company_email = fields.Char(string="Company email")

    @api.multi
    def create_company(self):
        """
        Set company email for the company this partner belongs to
        """
        res = super().create_company()

        print("COMPANY CREATED")
        print(res)
        print(self.company_email)

        if self.company_email:
            self.parent_id.email = self.company_email

        return res
