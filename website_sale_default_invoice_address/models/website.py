from odoo import models

import logging

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = "website"

    def _prepare_sale_order_values(self, partner_sudo):
        self.ensure_one()

        partner_obj = self.env["res.partner"]

        values = super()._prepare_sale_order_values(partner_sudo)

        invoice_address_to_use = False

        if partner_sudo.default_partner_invoice_id:
            # Check if partner has a default invoice address
            invoice_address_to_use = partner_sudo.default_partner_invoice_id.id
        elif partner_sudo.commercial_partner_id.default_partner_invoice_id:
            # Check if commercial partner has a default invoice address
            invoice_address_to_use = (
                partner_sudo.commercial_partner_id.default_partner_invoice_id.id
            )

        # Do a check to prevent using invoice addresses that would raise
        # error 403 in website_sale's address()
        if invoice_address_to_use:
            allowed_invoice_addresses = partner_obj.search(
                [("id", "child_of", partner_sudo.commercial_partner_id.ids)]
            )

            if invoice_address_to_use in [a.id for a in allowed_invoice_addresses]:
                values["partner_invoice_id"] = invoice_address_to_use
            else:
                _logger.debug(
                    "Skipped using invoice address id %s, partner %s "
                    "did not have access to it "
                    % (invoice_address_to_use, partner_sudo.id)
                )

        return values
