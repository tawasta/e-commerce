import logging
import re
from odoo import http
from odoo.http import request
from odoo.osv import expression

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super(WebsiteSale, self)._get_shop_payment_values(order, **kwargs)
        self._process_order_lines(order, values)
        #self._update_payment_acquirers(order, values)
        logging.info(values);
        return values

    def _process_order_lines(self, order, values):
        flags = {
            "allowed_methods": [],
            "check_mandatory_products": False,
            "check_attachment": False,
            "check_explanation": False,
            "check_category_product": False,
            "need_company_info": False,
            "product_categ_list": [],
            "mandatory_products_list": []
        }

        for line in order.order_line:
            self._check_order_line_flags(line, flags)

        self._update_values_based_on_flags(order, flags, values)

    def _check_order_line_flags(self, line, flags):
        product = line.product_id
        if product.allowed_payment_method_ids:
            flags["allowed_methods"].extend(product.allowed_payment_method_ids.ids)
        if product.mandatory_products:
            flags["check_mandatory_products"] = True
        if product.requires_attachment:
            flags["check_attachment"] = True
        if product.requires_explanation:
            flags["check_explanation"] = True
        if request.env.user.id == request.env.ref("base.public_user").id and product.required_product_category_id:
            flags["check_category_product"] = True
            flags["product_categ_list"].append(product.required_product_category_id)

    def _update_values_based_on_flags(self, order, flags, values):
        if flags["check_mandatory_products"]:
            mandatory_products_list = []
            for li in order.order_line:
                if li.product_id.mandatory_products:
                    for mp in li.product_id.mandatory_products:
                        mandatory_products_list.append(mp)
            values["mandatory_products_list"] = mandatory_products_list

        if flags["check_category_product"]:
            remaining_categories = set(flags["product_categ_list"])
            for product_line in order.order_line:
                for p_categ in product_line.product_id.public_categ_ids:
                    remaining_categories.discard(p_categ)
            values["product_categ_list"] = list(remaining_categories)


        if flags["check_attachment"] and order.message_attachment_count < 1:
            values["need_attachment"] = True

        cleaned_note = re.sub('<[^<]+?>', '', order.note).strip()
        if flags["check_explanation"] and not cleaned_note:
            values["need_explanation"] = True

        if flags["need_company_info"]:
            values["need_company_info"] = True

        allowed_methods_ids = set(flags["allowed_methods"])
        if allowed_methods_ids:
            values["payment_methods_sudo"] = request.env['payment.method'].browse(list(allowed_methods_ids))


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
        # response.qcontext["search_count"]
        # response.qcontext["attributes"]
        # response.qcontext["search"]
        product_list = []
        for p in products:
            if (
                not p.allowed_groups_ids
                or p.allowed_groups_ids in request.env.user.groups_id
            ):
                product_list.append(p.id)

        products_ids = (
            request.env["product.template"].sudo().search([("id", "in", product_list)])
        )
        logging.info(products_ids)
        response.qcontext.update(
            {
                "bins": TableCompute().process(
                    response.qcontext["products"],
                    response.qcontext["ppg"],
                    response.qcontext["ppr"],
                ),
                "products": products_ids,
            }
        )
        return response

    @http.route()
    def products_autocomplete(self, term, options=False, **kwargs):
        if not options:
            options = {}

        response = super(WebsiteSale, self).products_autocomplete(
            term, options=options, **kwargs
        )
        products = response["products"]
        product_list = []
        for i in range(len(products)):
            product = request.env["product.template"].search(
                [("id", "=", products[i]["id"])]
            )
            if product:
                if (
                    not product.allowed_groups_ids
                    or product.allowed_groups_ids in request.env.user.groups_id
                ):
                    product_list.append(products[i])

        response.update({"products": product_list, "products_count": len(product_list)})

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
                # if 21st products (index 20) and the last line is full (ppr products in it),
                # break (pos + 1.0) / ppr is the line where the product would be inserted
                # maxy is the number of existing lines
                # + 1.0 is because pos begins at 0, thus pos 20 is actually the 21st block
                # and to force python to not round the division operation
                if index >= ppg and ((pos + 1.0) // ppr) > maxy:
                    break

                if x == 1 and y == 1:  # simple heuristic for CPU optimization
                    minpos = pos // ppr

                for y2 in range(y):
                    for x2 in range(x):
                        self.table[(pos // ppr) + y2][(pos % ppr) + x2] = False
                self.table[pos // ppr][pos % ppr] = {
                    "product": p,
                    "x": x,
                    "y": y,
                    "ribbon": p.website_ribbon_id,
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
