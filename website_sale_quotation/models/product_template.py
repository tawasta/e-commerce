from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    list_price = fields.Float(groups="base.group_user")

    def _get_combination_info(self, *args, **kwargs):
        user = self.env.user
        if user.has_group("base.group_portal") or user.has_group("base.group_public"):
            # Public or portal users cannot see list prices,
            # se we'll need to use sudo for combination info
            self = self.sudo()

        return super(ProductTemplate, self)._get_combination_info(*args, **kwargs)
