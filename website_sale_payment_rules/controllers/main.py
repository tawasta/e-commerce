from odoo import http
from odoo.http import request
from odoo.osv import expression
import logging

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):  # noqa: max-complexity: 23
        values = super(WebsiteSale, self)._get_shop_payment_values(order, **kwargs)
        only_invoice = False
        need_company_info = False
        check_attachment = False
        check_explanation = False
        check_category_product = False
        check_mandatory_products = False
        product_categ_list = []
        mandatory_products_list = []
        companies = []
        for line in order.order_line:
            if line.product_id.membership_type == "company":
                if not order.partner_id.parent_id:
                    need_company_info = True
            if line.product_id.payment_only_invoice:
                only_invoice = True
            if line.product_id.mandatory_products:
                check_mandatory_products = True
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

        if check_mandatory_products:
            for li in order.order_line:
                if li.product_id.mandatory_products:
                    for mp in li.product_id.mandatory_products:
                        mandatory_products_list.append(mp)
            values.update({"mandatory_products_list": mandatory_products_list})

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
        sale_order_id = request.session.get("sale_last_order_id")
        company_id = False
        if sale_order_id:
            order = request.env["sale.order"].sudo().browse(sale_order_id)
            companies = []
            for line in order.order_line:
                companies.append(line.product_id.company_id)

            result = all(element == companies[0] for element in companies)

            if result:
                company_id = companies[0]
            else:
                company_id = request.env["res.company"]._get_main_company()

            if order.company_id != company_id:
                warehouse_id = (
                    request.env.user.with_company(company_id.id)
                    ._get_default_warehouse_id()
                    .id
                )
                fiscal_position_id = (
                    request.env["account.fiscal.position"]
                    .sudo()
                    .with_company(company_id.id)
                    .get_fiscal_position(
                        order.partner_id.id, order.partner_shipping_id.id
                    )
                )

                order.sudo().write(
                    {
                        "company_id": company_id,
                        "fiscal_position_id": fiscal_position_id.id,
                        "warehouse_id": warehouse_id,
                    }
                )

        return super(WebsiteSale, self).payment_confirmation(**post)

    @http.route()
    def shop(self, page=0, category=None, search="", ppg=False, **post):

        response = super(WebsiteSale, self).shop(
            page=page, category=category, search=search, ppg=ppg, **post
        )

        products = response.qcontext["products"]
        attrib_values = response.qcontext["search_count"]
        attributes = response.qcontext["attributes"]
        searches = response.qcontext["search"]
        product_list = [] 
        for p in products:
            if not p.allowed_groups_ids or p.allowed_groups_ids in request.env.user.groups_id:
                product_list.append(p.id)

        products_ids = (
            request.env["product.template"]
            .sudo()
            .search([("id", "in", product_list)])
        )
        logging.info(products_ids)
        response.qcontext.update({
            "bins": TableCompute().process(response.qcontext["products"], response.qcontext["ppg"], response.qcontext["ppr"]),
            "products": products_ids,
        })
        return response

    @http.route()
    def products_autocomplete(self, term, options={}, **kwargs):

        response = super(WebsiteSale, self).products_autocomplete(
            term, options=options, **kwargs
        )
        products = response["products"]
        product_list = []
        for i in range(len(products)):
            product = request.env["product.template"].search([
                ('id', '=', products[i]['id'])
            ])
            if product:
                if not product.allowed_groups_ids or product.allowed_groups_ids in request.env.user.groups_id:
                    product_list.append(products[i])

        response.update({
            'products': product_list,
            'products_count': len(product_list)
        })

        return response

class TableCompute(object):

    def __init__(self):
        self.table = {}

    def _check_place(self, posx, posy, sizex, sizey, ppr):
        res = True
        for y in range(sizey):
            for x in range(sizex):
                if posx + x >= ppr:
                    res = False
                    break
                row = self.table.setdefault(posy + y, {})
                if row.setdefault(posx + x) is not None:
                    res = False
                    break
            for x in range(ppr):
                self.table[posy + y].setdefault(x, None)
        return res

    def process(self, products, ppg=20, ppr=4):
        # Compute products positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        x = 0
        groups_ids = request.env.user.groups_id
        for p in products:
            if not p.allowed_groups_ids or p.allowed_groups_ids in groups_ids:

                x = min(max(p.website_size_x, 1), ppr)
                y = min(max(p.website_size_y, 1), ppr)
                if index >= ppg:
                    x = y = 1

                pos = minpos
                while not self._check_place(pos % ppr, pos // ppr, x, y, ppr):
                    pos += 1
                # if 21st products (index 20) and the last line is full (ppr products in it), break
                # (pos + 1.0) / ppr is the line where the product would be inserted
                # maxy is the number of existing lines
                # + 1.0 is because pos begins at 0, thus pos 20 is actually the 21st block
                # and to force python to not round the division operation
                if index >= ppg and ((pos + 1.0) // ppr) > maxy:
                    break

                if x == 1 and y == 1:   # simple heuristic for CPU optimization
                    minpos = pos // ppr

                for y2 in range(y):
                    for x2 in range(x):
                        self.table[(pos // ppr) + y2][(pos % ppr) + x2] = False
                self.table[pos // ppr][pos % ppr] = {
                    'product': p, 'x': x, 'y': y,
                    'ribbon': p.website_ribbon_id,
                }
                if index <= ppg:
                    maxy = max(maxy, y + (pos // ppr))
                index += 1

        # Format table according to HTML needs
        rows = sorted(self.table.items())
        rows = [r[1] for r in rows]
        for col in range(len(rows)):
            cols = sorted(rows[col].items())
            x += len(cols)
            rows[col] = [r[1] for r in cols if r[1]]

        return rows