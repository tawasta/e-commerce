from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    customer_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="customer_product_rel",
        column1="customer_id",
        column2="product_id",
        string="Replace for customers",
    )

    replace_product_id = fields.Many2one(
        comodel_name="product.template",
        string="Replace this product",
        help="Show this product in shop instead. If no customers are selected, "
             "the product is replaced for everyone"
    )

    replacement_ids = fields.One2many(
        comodel_name="product.template",
        inverse_name="replace_product_id",
        string="Replacing products",
        readonly=True,
    )
