import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProductPublicCategory(models.Model):

    _inherit = "product.public.category"

    show_as_external_link = fields.Boolean(
        string="Show as External Link",
        help="Check if you want this category to be shown as a link on website, "
        "instead of it containing products like a regular category.",
    )

    external_link_url = fields.Char(
        string="External Link URL", help="The address where the link will point to"
    )
