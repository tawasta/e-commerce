from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_new_no_code_promo_reward_lines(self):
        all_lines = False
        if self.order_line:
            all_lines = self.order_line

        values = super(SaleOrder, self)._create_new_no_code_promo_reward_lines()
        if all_lines:
            website = self.env["website"].get_current_website()
            new_lines = list(set(self.order_line) - set(all_lines))
            for record in new_lines:
                if website.company_id != record.product_id.company_id:
                    company_id = record.product_id.company_id
                    record = record.with_company(company_id)
                    fpos = (
                        record.order_id.fiscal_position_id
                        or record.order_id.fiscal_position_id.get_fiscal_position(
                            record.order_partner_id.id
                        )
                    )
                    # If company_id is set, always filter taxes by the company
                    taxes = record.product_id.taxes_id.filtered(
                        lambda t: t.company_id == record.env.company
                    )
                    tax_id = fpos.map_tax(
                        taxes, record.product_id, record.order_id.partner_shipping_id
                    )
                    record.sudo().write({"tax_id": tax_id})

        return values
