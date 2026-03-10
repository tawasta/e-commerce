import logging

from odoo import api, models
from odoo.tools.misc import split_every

_logger = logging.getLogger(__name__)


class WooProductTemplateEpt(models.Model):
    _inherit = "woo.product.template.ept"

    @api.model
    def cron_export_stock_in_woo(self):
        templates = (
            self.sudo()
            .search(
                [
                    ("exported_in_woo", "=", True),
                    ("active", "=", True),
                    ("woo_instance_id.active", "=", True),
                    ("woo_tmpl_id", "!=", False),
                ]
            )
            .ids
        )

        if not templates:
            _logger.info("Woo stock export cron: nothing to export.")
            return True

        Wizard = self.env["woo.process.import.export"].sudo()

        for chunk in split_every(80, templates):
            ctx = dict(
                self.env.context,
                active_model="woo.product.template.ept",
                active_ids=chunk,
            )
            wiz = Wizard.with_context(**ctx).create({})
            wiz.with_context(**ctx).export_stock_in_woo()

        return True
