import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):

    _inherit = "product.template"

    website_page_canonical_link_target_id = fields.Many2one(
        comodel_name="website.page",
        string="Canonical Link Target",
        help="Bypass Odoo's default link rel='canonical' link creation "
        "for this product's page, and have the link point to a custom page instead.",
    )
