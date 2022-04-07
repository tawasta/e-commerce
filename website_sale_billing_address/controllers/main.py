from odoo.http import request
from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleBilling(WebsiteSale):

    @http.route()
    def address(self, **kw):
        response = super(WebsiteSaleBilling, self).address(**kw)
        order = request.website.sale_get_order()
        if 'submitted' in kw:
            if not kw.get('billing_use_same') and not order.only_services:
                order.sudo().write({'use_different_billing_address': True})

                return response
            else:
                return response
        else:
            return response

    @http.route()
    def confirm_order(self, **post):
        order = request.website.sale_get_order()
        if order.use_different_billing_address:
            return request.redirect("/shop/billing_address")
        else:
            return super(WebsiteSaleBilling, self).confirm_order(**post)

    @http.route()
    def extra_info(self, **post):
        order = request.website.sale_get_order()
        if order.use_different_billing_address and order.partner_id == order.partner_invoice_id:
            return request.redirect("/shop/billing_address")
        else:
            return super(WebsiteSaleBilling, self).extra_info(**post)

    @http.route(['/shop/billing_address'], type='http', auth="public", website=True, sitemap=False)
    def billing_address(self, **post):
        order = request.website.sale_get_order()

        # check that cart is valid
        order = request.website.sale_get_order()
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection
        countries = request.env["res.country"].sudo().search([])
        company_vals = {}
        current_user = request.env.user
        if 'submitted' in post:
            country = request.env['res.country'].browse(int(post.get("c_id")))
            partner_vals = {
                'name': post.get("name"),
                'phone': post.get("phone"),
                'street': post.get("street"),
                'street2': post.get("street2"),
                'zip': post.get("zip"),
                'city': post.get("city"),
                'country_id': country.id,
            }
            if post.get("company_name"):
                company_vals.update({
                    'name': post.get("company_name"),
                    'email': post.get("company_email"),
                    'vat': post.get("vat"),
                    'edicode': post.get("edicode") or False,
                    'einvoice_operator_id': post.get("einvoice_operator_id") or False
                })

            if 'editing' in post:
                current_partner = request.env["res.partner"].sudo().search([
                    ('id', '=', post.get("partner_id"))
                ])
                if current_partner == order.partner_invoice_id:
                    current_partner.sudo().write(partner_vals)

                if post.get("company_id"):
                    current_company = request.env["res.partner"].sudo().search([
                        ('id', '=', post.get("company_id"))
                    ])
                    current_company.sudo().write(company_vals)
                    if company_vals and not current_company:
                        company_vals.update({
                            'is_company': True
                        })
                        company = request.env["res.partner"].sudo().create(company_vals)
                        current_partner.sudo().write({'parent_id': company.id})
            else:
                partner_id = request.env["res.partner"].sudo().create(partner_vals)

                if company_vals:
                    company_vals.update({
                        'is_company': True
                    })
                    company = request.env["res.partner"].sudo().create(company_vals)
                    partner_id.sudo().write({'parent_id': company.id})


                order.sudo().write({'partner_invoice_id': partner_id})

            if current_user.partner_id == order.partner_id:
                if not order.use_different_billing_address:
                    order.sudo().write({'use_different_billing_address': True})
            if 'submitted' in post and not 'editing' in post:
                if not order.use_different_billing_address:
                    order.sudo().write({'use_different_billing_address': True})

            return request.redirect("/shop/extra_info")



        values = {
            'website_sale_order': order,
            'countries': countries,
            'order': order,
        }
        if order.use_different_billing_address and order.partner_invoice_id != order.partner_id:
            values.update({
                'partner': order.partner_invoice_id
            })

        return request.render("website_sale_billing_address.billing_address", values)

    def checkout_redirection(self, order):
        # must have a draft sales order with lines at this point, otherwise reset
        if not order or order.state != 'draft':
            request.session['sale_order_id'] = None
            request.session['sale_transaction_id'] = None
            return request.redirect('/shop')

        if order and not order.order_line:
            return request.redirect('/shop/cart')

        # if transaction pending / done: redirect to confirmation
        tx = request.env.context.get('website_sale_transaction')
        if tx and tx.state != 'draft':
            return request.redirect('/shop/payment/confirmation/%s' % order.id)

