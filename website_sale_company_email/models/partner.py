from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    company_email = fields.Char(string="Company email")

    def create_company(self):
        """
        Set company email for the company this partner belongs to
        """
        res = super().create_company()

        if self.company_email:
            self.parent_id.email = self.company_email

        return res
