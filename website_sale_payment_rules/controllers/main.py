from odoo.http import request
from odoo.osv import expression
from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super(WebsiteSale, self)._get_shop_payment_values(order, **kwargs)
        only_invoice = False
        need_company_info = False
        check_attachment = False
        check_explanation = False
        check_category_product = False
        product_categ_list = []
        companies = []
        for line in order.order_line:
            if line.product_id.membership_type == 'company':
                if not order.partner_id.parent_id:
                    need_company_info = True
            if line.product_id.payment_only_invoice:
                only_invoice = True
            if line.product_id.requires_attachment:
                check_attachment = True
            if line.product_id.requires_explanation:
                check_explanation = True
            if request.env.user.id == request.env.ref("base.public_user").id:
                if line.product_id.required_product_category_id:
                    check_category_product = True
                    product_categ_list.append(
                        line.product_id.required_product_category_id
                    )
            companies.append(line.product_id.company_id)

        result = all(element == companies[0] for element in companies)
        if not result:
            only_invoice = True
        if result:
            company_id = companies[0]

        if check_category_product:
            for product_line in order.order_line:
                for p_categ_id in product_line.product_id.public_categ_ids:
                    if p_categ_id in product_categ_list:
                        product_categ_list.remove(p_categ_id)
            if product_categ_list:
                values.update({"product_categ_list": product_categ_list})

        if check_attachment:
            if order.message_attachment_count < 1:
                values.update({"need_attachment": True})
        if check_explanation:
            if not order.note:
                values.update({"need_explanation": True})
        if need_company_info:
            values.update({"need_company_info": True})

        if only_invoice:
            domain = expression.AND(
                [
                    [
                        ("provider", "!=", "paytrail"),
                        "&",
                        ("state", "in", ["enabled", "test"]),
                        ("company_id", "=", order.company_id.id),
                    ],
                    [
                        "|",
                        ("website_id", "=", False),
                        ("website_id", "=", request.website.id),
                    ],
                    [
                        "|",
                        ("country_ids", "=", False),
                        ("country_ids", "in", [order.partner_id.country_id.id]),
                    ],
                ]
            )

        else:
            domain = expression.AND(
                [
                    [
                        ("state", "in", ["enabled", "test"]),
                        ("company_id", "=", company_id.id),
                    ],
                    [
                        "|",
                        ("website_id", "=", False),
                        ("website_id", "=", request.website.id),
                    ],
                    [
                        "|",
                        ("country_ids", "=", False),
                        ("country_ids", "in", [order.partner_id.country_id.id]),
                    ],
                ]
            )
        acquirers = request.env["payment.acquirer"].search(domain)
        values["acquirers"] = acquirers

        return values

    @http.route()
    def payment_confirmation(self, **post):
        sale_order_id = request.session.get('sale_last_order_id')
        company_id = False
        if sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            companies = []
            for line in order.order_line:
                companies.append(line.product_id.company_id)

            result = all(element == companies[0] for element in companies)

            if result:
                company_id = companies[0]
            else:
                company_id = request.env['res.company']._get_main_company()

            if order.company_id != company_id:
                warehouse_id = request.env.user.with_company(company_id.id)._get_default_warehouse_id().id
                fiscal_position_id = request.env['account.fiscal.position'].sudo().with_company(company_id.id).get_fiscal_position(order.partner_id.id, order.partner_shipping_id.id)
                print(fiscal_position_id)
                order.sudo().write({
                    'company_id': company_id,
                    'fiscal_position_id': fiscal_position_id.id,
                    'warehouse_id': warehouse_id,
                })

                for order_line in order.order_line:
                    order_line = order_line.with_company(company_id)
                    fpos = order_line.order_id.fiscal_position_id or order_line.order_id.fiscal_position_id.get_fiscal_position(order_line.order_partner_id.id)
                    # If company_id is set, always filter taxes by the company
                    taxes = line.product_id.taxes_id.filtered(lambda t: t.company_id == line.env.company)
                    tax_id = fpos.map_tax(taxes, line.product_id, line.order_id.partner_shipping_id)
                    order_line.sudo().write({'tax_id': tax_id})

        return super(WebsiteSale, self).payment_confirmation(**post)
