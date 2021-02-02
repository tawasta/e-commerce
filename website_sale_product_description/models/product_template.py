from odoo import api
from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def write(self, vals):
        res = super().write(vals)

        if "website_description" in vals:
            for record in self:
                self.env["ir.translation"].translate_fields(
                    "product.template", record.id, "website_description"
                )

        return res
