from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    website_cart_note = fields.Html(
        string="Website cart note",
        help="Note that is show in cart"
    )
