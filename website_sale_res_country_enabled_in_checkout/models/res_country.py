import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResCountry(models.Model):
    _inherit = "res.country"

    ecommerce_published = fields.Boolean(
        string="Show in eCommerce Country Selection",
        help="Adds this country to selectable countries in eCommerce checkout",
        default=False,
    )

    def get_website_sale_countries(self, mode="billing"):
        """Filter out countries that should not be shown"""
        res = super().get_website_sale_countries(mode=mode)
        return res.filtered(lambda c: c.ecommerce_published)
