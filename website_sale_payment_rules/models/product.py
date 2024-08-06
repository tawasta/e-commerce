from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    change_allowed = fields.Boolean(string="Change allowed", default=False)

    allowed_groups_ids = fields.Many2many(
        string="Allowed groups can see the product", comodel_name="res.groups"
    )

    mandatory_products = fields.Many2many(
        comodel_name="product.product",
        relation="mandatory_product_product_rel",
        string="Mandatory products",
    )
