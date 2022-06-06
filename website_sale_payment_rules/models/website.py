from odoo import fields, models
from odoo.http import request


class Website(models.Model):
    _inherit = "website"

    add_explanation_text = fields.Html(
        string="Website sale: add an explanation", readonly=False, translate=True
    )

    add_attachment_text = fields.Html(
        string="Website sale: add an attachment", readonly=False, translate=True
    )

    product_categ_text = fields.Html(
        string="Website sale: Required product category text",
        readonly=False,
        translate=True,
    )

    company_info_text = fields.Html(
        string="Website sale: need company data", readonly=False, translate=True
    )

    def sale_get_order(self, *args, **kwargs):
        # Override to allow fixing SO taxes on multi-company website
        res = super().sale_get_order(*args, **kwargs)

        sale_order_id = request.session.get("sale_order_id")
        sale_order = (
            self.env["sale.order"]
            .with_company(request.website.company_id.id)
            .sudo()
            .browse(sale_order_id)
            .exists()
            if sale_order_id
            else None
        )

        if not sale_order:
            return res

        for order_line in sale_order.order_line:
            if order_line.company_id == sale_order.company_id:
                continue

            company_id = order_line.product_id.company_id
            order_line = order_line.with_company(company_id)

            fpos = (
                order_line.order_id.fiscal_position_id
                or order_line.order_id.fiscal_position_id.get_fiscal_position(
                    order_line.order_partner_id.id
                )
            )
            # If company_id is set, always filter taxes by the company
            taxes = order_line.product_id.taxes_id.filtered(
                lambda t: t.company_id == order_line.env.company
            )
            tax_id = fpos.map_tax(
                taxes, order_line.product_id, order_line.order_id.partner_shipping_id
            )
            order_line.sudo().write({"tax_id": tax_id})

        return res
