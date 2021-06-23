from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_id = fields.Many2one(
        'product.product', string='Product', domain="[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        change_default=True, ondelete='restrict', check_company=False)  # Unrequired company

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_invoices(self, grouped=False, final=False):
        companies = []
        for line_product in self.order_line:
            companies.append(line_product.product_id.company_id)

        result = all(element == companies[0] for element in companies)

        if result:
            return super()._create_invoices(grouped=grouped, final=final)
        else:
            print("======LISTALLE ON ERI YRITYKSIÄ=======")

            company_list = list(dict.fromkeys(companies))
            # print(new_list)
            for company in company_list:
                invoice_vals_list = []
                print(company)
                invoice_vals = self._prepare_invoice()
                invoice_vals.update({
                    "partner_bank_id": company.partner_id.bank_ids[:1].id,
                    "company_id": company.id,
                })
                print(invoice_vals)
                for line in self.order_line:
                    if line.product_id.company_id == company:
                        invoice_vals_list.append(line)
                # for line in self.sale_order_line:
                #     if line.company_id == company:


            # invoice_ids = super()._create_invoices(grouped=grouped, final=final)
            # for invoice in invoice_ids:
            #     print(invoice)
            #     new_invoice = invoice.copy()
            #     print(new_invoice)
            #     for invoice_line in invoice.invoice_line_ids:
            #         if not invoice_line.product_id.company_id == invoice.company_id:
            #             journal = self.env["account.journal"].sudo().search([
            #                 ('company_id', '=', invoice_line.product_id.company_id.id)
            #             ])
            #             account_id = self.env["account.account"].sudo().search([
            #                 ('company_id', '=', invoice_line.product_id.company_id.id)
            #             ])
            #             fiscal_position_id = self.env["account.fiscal.position"].sudo().search([
            #                 ('company_id', '=', invoice_line.product_id.company_id.id)
            #             ])
            #             new_invoice.write({'line_ids': [(2, c.id) for c in new_invoice.line_ids]})
            #             new_invoice.sudo().write({"company_id": invoice_line.product_id.company_id.id, "journal_id": journal.id, "fiscal_position_id": fiscal_position_id.id})

            #             invoice_line.sudo().write({"move_id": new_invoice.id, "account_id": account_id.id})
                # for li in new_list:

            # for invoice in invoice_ids:

            # for invoice in invoice_ids:

        # for invoice in invoice_ids:
        #     contract_so = (
        #         self.env["sale.order"]
        #         .sudo()
        #         .search([("invoice_ids", "in", invoice.ids)])
        #     )
        #     if contract_so:
        #         invoice.sudo().write({"old_contract_id": contract_so.contract_id.id})

        # return invoice_ids


# def _prepare_invoice_values(self, order, name, amount, so_line):
#         invoice_vals = {
#             'ref': order.client_order_ref,
#             'move_type': 'out_invoice',
#             'invoice_origin': order.name,
#             'invoice_user_id': order.user_id.id,
#             'narration': order.note,
#             'partner_id': order.partner_invoice_id.id,
#             'fiscal_position_id': (order.fiscal_position_id or order.fiscal_position_id.get_fiscal_position(order.partner_id.id)).id,
#             'partner_shipping_id': order.partner_shipping_id.id,
#             'currency_id': order.pricelist_id.currency_id.id,
#             'payment_reference': order.reference,
#             'invoice_payment_term_id': order.payment_term_id.id,
#             'partner_bank_id': order.company_id.partner_id.bank_ids[:1].id,
#             'team_id': order.team_id.id,
#             'campaign_id': order.campaign_id.id,
#             'medium_id': order.medium_id.id,
#             'source_id': order.source_id.id,
#             'invoice_line_ids': [(0, 0, {
#                 'name': name,
#                 'price_unit': amount,
#                 'quantity': 1.0,
#                 'product_id': self.product_id.id,
#                 'product_uom_id': so_line.product_uom.id,
#                 'tax_ids': [(6, 0, so_line.tax_id.ids)],
#                 'sale_line_ids': [(6, 0, [so_line.id])],
#                 'analytic_tag_ids': [(6, 0, so_line.analytic_tag_ids.ids)],
#                 'analytic_account_id': order.analytic_account_id.id or False,
#             })],
#         }

#         return invoice_vals