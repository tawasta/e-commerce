from odoo.http import request
from odoo.osv import expression

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super(WebsiteSale, self)._get_shop_payment_values(order, **kwargs)
        only_invoice = False
        check_attachment = False
        check_explanation = False
        check_category_product = False
        product_categ_list = []
        companies = []
        for line in order.order_line:
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
