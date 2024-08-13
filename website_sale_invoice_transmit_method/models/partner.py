from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def create_company(self):
        transmit_method = self.customer_invoice_transmit_method_id
        res = super().create_company()

        if self.parent_id:
            # Add Transmit method to parent
            self.parent_id.customer_invoice_transmit_method_id = transmit_method.id
        return res
