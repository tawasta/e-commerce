from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    hide_company_slider = fields.Boolean(
        "Hide company slider",
        compute="_compute_hide_company_slider",
    )

    force_company_slider = fields.Boolean(
        "Force company slider", compute="_compute_hide_company_slider"
    )

    def _compute_hide_company_slider(self):
        for record in self:
            force_slider = record.order_line.mapped("product_id.force_company_slider")
            hide_slider = record.order_line.mapped("product_id.hide_company_slider")

            record.force_company_slider = True in force_slider
            record.hide_company_slider = True in hide_slider or True in force_slider
