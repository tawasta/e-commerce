from odoo import fields, models


class SuggestedProductsCategory(models.Model):
    _name = "suggested.products.category"
    _inherit = [
        "website.multi.mixin",
    ]
    _description = "Suggested Accessory Products Category"
    _order = "sequence, name, id"

    name = fields.Char(
        "Suggested Accessory Products Category", required=True, translate=True
    )
    sequence = fields.Integer(default=1)
    description = fields.Text(
        required=True,
        translate=True,
        help="Description displayed for the suggested accessory products "
        "category on the website.",
    )
    product_public_category_ids = fields.One2many(
        comodel_name="product.public.category",
        inverse_name="suggested_products_category_id",
        string="eCommerce Categories",
        help="Products from these eCommerce Categories will be included under this "
        "Suggested Accessory Products Category.",
    )
    product_ids = fields.Many2many(
        "product.product", "Products", compute="_compute_product_ids"
    )

    def _compute_product_ids(self):
        for rec in self:
            products = self.env["product.product"].search(
                [["public_categ_ids", "in", rec.product_public_category_ids.ids]]
            )
            rec.product_ids = products
