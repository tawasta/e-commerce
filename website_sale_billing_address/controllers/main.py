from odoo.http import request
from urllib.parse import urlparse
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
            print("=====KAYKO TAALLA VAI NYT=====")
            return request.redirect("/shop/billing_address")
        else:
            return super(WebsiteSaleBilling, self).extra_info(**post)

    def checkout_values(self, **kw):
        response = super(WebsiteSaleBilling, self).checkout_values(**kw)
        order = request.website.sale_get_order(force_create=1)
        billings = []
        if order.partner_id != request.website.user_id.sudo().partner_id:
            Partner = order.partner_id.with_context(show_address=1).sudo()
            childs = Partner.search([
                ("id", "=", order.partner_id.id),
                # ("type", "in", ["invoice"])
            ]).mapped('child_ids')

            billing_partners = Partner.search([
                ('id', 'in', childs.ids),
                ('type', '=', 'invoice'),
            ], order='id desc')

            print(order.partner_id)
            print(billing_partners)
            for bp in billing_partners:
                if bp.is_company and bp.child_ids:
                    for c in bp.child_ids:
                        billings.append(c)
                if bp.is_company and not bp.child_ids:
                    billings.append(bp)
                if not bp.is_company:
                    billings.append(bp)

            billings.append(order.partner_id)
            print(billings)
            response.update({'billings': billings})

        return response

    @http.route(['/shop/change/billing_address'], type='http', auth="public", website=True, sitemap=False)
    def change_billing_address(self, **post):
        order = request.website.sale_get_order()

        # check that cart is valid
        order = request.website.sale_get_order()
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        if 'partner_id' in post and 'user_billing_address' in post:
            partner_id = request.env["res.partner"].sudo().search([
                ('id', '=', post.get('partner_id'))
            ])
            order.sudo().write({
                'partner_invoice_id': partner_id
            })

            return request.redirect(post.get('return_url'))

    @http.route(['/shop/billing_address', '/shop/billing_address/<int:partner_id>'], type='http', auth="public", website=True, sitemap=False)
    def billing_address(self, partner_id=None, **post):
        order = request.website.sale_get_order()
        print(post)

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
                'type': 'invoice',
                'zip': post.get("zip"),
                'city': post.get("city"),
                'country_id': country.id,
            }
            if post.get("company_name"):
                company_vals.update({
                    'name': post.get("company_name"),
                    'email': post.get("company_email"),
                    'vat': post.get("vat"),
                    'type': 'invoice',
                    'edicode': post.get("edicode") or False,
                    'einvoice_operator_id': post.get("einvoice_operator_id") or False
                })

            if 'editing' in post:
                current_partner = request.env["res.partner"].sudo().search([
                    ('id', '=', post.get("partner_id"))
                ])

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
                    company.sudo().write({'parent_id': order.partner_id.id})

                else:
                    partner_id.sudo().write({'parent_id': order.partner_id.id})



                order.sudo().write({'partner_invoice_id': partner_id})

            if current_user.partner_id == order.partner_id and not partner_id:
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
        if 'new_billing_address' in post:
            print("=====TAMA=====")
            values.update({
                'partner': False
            })
        if order.use_different_billing_address and order.partner_invoice_id != order.partner_id and not 'new_billing_address' in post:
            values.update({
                'partner': order.partner_invoice_id
            })

        if partner_id:
            allow_partner_edit = False
            edit_partner = request.env["res.partner"].sudo().search([
                ('id', '=', partner_id)
            ])
            if edit_partner in order.partner_id.child_ids:
                allow_partner_edit = True
                values.update({
                    'partner': edit_partner
                })
            else:
                # TAHAN JOKIN VIRHE ETTÄ EI MUUTEN ONNISTU

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

