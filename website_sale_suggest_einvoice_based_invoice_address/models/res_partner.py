from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _find_einvoicing_invoice_partner(self):
        """Attempt to find an address for the partner:
        First partner under the same commercial partner with both edicode
        and einvoice_operator_id set. Considers invoice-type children plus
        the commercial partner itself. Returns empty recordset if none qualify."""
        self.ensure_one()
        commercial = self.commercial_partner_id
        return self.env["res.partner"].search(
            [
                ("id", "child_of", commercial.id),
                "|",
                ("type", "=", "invoice"),
                ("id", "=", commercial.id),
                ("edicode", "!=", False),
                ("einvoice_operator_id", "!=", False),
            ],
            limit=1,
        )
