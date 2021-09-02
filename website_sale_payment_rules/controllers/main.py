# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
from odoo.osv import expression


class WebsiteSale(WebsiteSale):

    def _get_shop_payment_values(self, order, **kwargs):
        values = super(WebsiteSale, self)._get_shop_payment_values(order, **kwargs)
        only_invoice = False
        companies = []
        for line in order.order_line:
            if line.product_id.payment_only_invoice:
                only_invoice = True
            companies.append(line.product_id.company_id)

        result = all(element == companies[0] for element in companies)
        if not result:
            only_invoice = True

        if only_invoice:
            domain = expression.AND([
                [('provider', '!=', 'paytrail'), '&', ('state', 'in', ['enabled', 'test']), ('company_id', '=', order.company_id.id)],
                ['|', ('website_id', '=', False), ('website_id', '=', request.website.id)],
                ['|', ('country_ids', '=', False), ('country_ids', 'in', [order.partner_id.country_id.id])]
            ])
            acquirers = request.env['payment.acquirer'].search(domain)
            values['acquirers'] = acquirers

        return values
