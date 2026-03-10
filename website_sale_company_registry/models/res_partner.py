import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    def create_company(self):
        # Set the company registry for parent company and also build VAT code from it

        company_registry = self.company_registry

        res = super().create_company()

        if company_registry:
            self.parent_id.company_registry = company_registry
            self.parent_id._compute_vat_from_company_registry()

        return res
