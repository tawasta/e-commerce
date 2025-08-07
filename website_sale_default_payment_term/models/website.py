from odoo import api, models


class Website(models.Model):
    _inherit = "website"

    @api.model
    def sale_get_payment_term(self, partner):
        payment_term = super().sale_get_payment_term(partner)

        default_payment_term = self.company_id.sale_default_payment_term

        pt = self.env.ref("account.account_payment_term_immediate", False)
        if pt:
            pt = pt.sudo()
            pt = (not pt.company_id.id or self.company_id.id == pt.company_id.id) and pt

        if payment_term == pt.id and default_payment_term:
            return default_payment_term.id
        else:
            return payment_term
