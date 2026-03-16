from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def create_company(self):
        res = super().create_company()

        if self.parent_id:
            if not self.parent_id.edicode:
                # Add edicode to parent
                self.parent_id.edicode = self.edicode

            if self.parent_id.edicode:
                # Remove edicode from contact
                self.edicode = False

            if not self.parent_id.einvoice_operator_id:
                # Add operator to parent
                self.parent_id.einvoice_operator_id = self.einvoice_operator_id

            if self.parent_id.einvoice_operator_id:
                # Remove operator from contact
                self.einvoice_operator_id = False

        return res
