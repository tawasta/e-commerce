from odoo import models

import logging

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = "website"

    def _prepare_sale_order_values(self, partner_sudo):
        self.ensure_one()

        _logger.info("_prepare_sale_order_values reached")
        values = super()._prepare_sale_order_values(partner_sudo)

        if partner_sudo.default_partner_invoice_id:
            # Check if partner has a default invoice address
            values["partner_invoice_id"] = partner_sudo.default_partner_invoice_id.id
        elif partner_sudo.commercial_partner_id.default_partner_invoice_id:
            # Check if commercial partner has a default invoice address
            values[
                "partner_invoice_id"
            ] = partner_sudo.commercial_partner_id.default_partner_invoice_id.id

        return values
