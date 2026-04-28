from odoo import models


class Website(models.Model):
    _inherit = "website"

    def _prepare_sale_order_values(self, partner_sudo):
        values = super()._prepare_sale_order_values(partner_sudo)
        einvoice_partner_suggestion = partner_sudo._find_einvoicing_invoice_partner()
        if einvoice_partner_suggestion:
            values["partner_invoice_id"] = einvoice_partner_suggestion.id
        return values
