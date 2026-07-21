from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def create_company(self):
        res = super().create_company()

        if self.parent_id:
            if not self.parent_id.customer_invoice_transmit_method_id:
                # Add Transmit method to parent
                self.parent_id.customer_invoice_transmit_method_id = (
                    self.customer_invoice_transmit_method_id
                )
        return res
