# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_portal_sale.controllers.main import website_account


class WebsiteAccountNoInvoices(website_account):

    @http.route()
    def portal_my_invoices(self, page=1, date_begin=None, 
                           date_end=None, **kw):
        # Override the route for listing all invoices / inspecting 
        # a single invoice
        return request.redirect('/my/home')

    @http.route()
    def portal_get_invoice(self, invoice_id=None, **kw):
        # Override the route for getting a single invoice's PDF print
        return request.redirect('/my/home')
