from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    create_user_attachment = fields.Many2one(string="Extra attachment to create user", comodel_name="ir.attachment")

    allow_create_user = fields.Boolean(default=False, string="Allow create user")
