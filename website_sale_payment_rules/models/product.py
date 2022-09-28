from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    payment_only_invoice = fields.Boolean("Payment by invoice only")

    requires_attachment = fields.Boolean("Requires an attachment")

    requires_explanation = fields.Boolean("Requires an explanation")

    required_product_category_id = fields.Many2one(
        string="Required product category", comodel_name="product.public.category"
    )

    company_id = fields.Many2one("res.company", "Company", index=1, required=True)

    change_allowed = fields.Boolean(string="Change allowed", default=False)

    mandatory_products = fields.Many2many(
        comodel_name="product.product",
        relation="mandatory_product_product_rel",
        string="Mandatory products",
    )
