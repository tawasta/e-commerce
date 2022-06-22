from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleBilling(WebsiteSale):
    @http.route()
    def address(self, **kw):
        new_billing = False
        order = request.website.sale_get_order()
        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            new_billing = True
        response = super(WebsiteSaleBilling, self).address(**kw)
        order = request.website.sale_get_order()
        if "submitted" in kw:
            if not kw.get("billing_use_same") and new_billing:
                print("====TRUE====")
                order.sudo().write({"use_different_billing_address": True})

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
        if (
            order.use_different_billing_address
            and order.partner_id == order.partner_invoice_id
        ):
            return request.redirect("/shop/billing_address")
        else:
            return super(WebsiteSaleBilling, self).extra_info(**post)

    def checkout_values(self, **kw):
        response = super(WebsiteSaleBilling, self).checkout_values(**kw)
        order = request.website.sale_get_order(force_create=1)
        billings = []
        if order.partner_id != request.website.user_id.sudo().partner_id:
            Partner = order.partner_id.with_context(show_address=1).sudo()
            childs = Partner.search(
                [
                    ("id", "=", order.partner_id.id),
                ]
            ).mapped("child_ids")

            billing_partners = Partner.search(
                [
                    ("id", "in", childs.ids),
                    ("type", "=", "invoice"),
                ],
                order="id desc",
            )

            for bp in billing_partners:
                if bp.is_company and bp.child_ids:
                    for c in bp.child_ids:
                        billings.append(c)
                if bp.is_company and not bp.child_ids:
                    billings.append(bp)
                if not bp.is_company:
                    billings.append(bp)

            billings.append(order.partner_id)
            response.update({"billings": billings})

        return response

    @http.route(
        ["/shop/change/billing_address"],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def change_billing_address(self, **post):
        order = request.website.sale_get_order()

        # check that cart is valid
        order = request.website.sale_get_order()
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        if "partner_id" in post and "user_billing_address" in post:
            partner_id = (
                request.env["res.partner"]
                .sudo()
                .search([("id", "=", post.get("partner_id"))])
            )
            order.sudo().write({"partner_invoice_id": partner_id})

            return request.redirect(post.get("return_url"))

    @http.route(
        ["/shop/billing_address", "/shop/billing_address/<int:partner_id>"],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def billing_address(self, partner_id=None, **post):
        order = request.website.sale_get_order()

        # check that cart is valid
        order = request.website.sale_get_order()
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection
        countries = request.env["res.country"].sudo().search([])
        company_vals = {}
        current_user = request.env.user
        if "submitted" in post:
            current_partner = (
                request.env["res.partner"]
                .sudo()
                .search([("id", "=", partner_id)])
            )
            print(current_partner)
            country = request.env["res.country"].browse(int(post.get("c_id")))
            partner_vals = {
                "firstname": post.get("firstname"),
                "lastname": post.get("lastname"),
                "phone": post.get("phone"),
                "street": post.get("street"),
                "street2": post.get("street2"),
                "type": "invoice",
                "zip": post.get("zip"),
                "city": post.get("city"),
                "country_id": country.id,
            }
            if post.get("company_name"):
                company_vals.update(
                    {
                        "name": post.get("company_name"),
                        "email": post.get("company_email"),
                        "vat": post.get("vat"),
                        "type": "invoice",
                        "edicode": post.get("edicode") or False,
                        "einvoice_operator_id": post.get("einvoice_operator_id")
                        or False,
                    }
                )

            print(current_partner)
            print(order.partner_id)
            if "editing" in post and current_partner != order.partner_id:
                print("====ABC=====")

                current_partner.sudo().write(partner_vals)

                if post.get("company_id"):
                    current_company = (
                        request.env["res.partner"]
                        .sudo()
                        .search([("id", "=", post.get("company_id"))])
                    )
                    current_company.sudo().write(company_vals)
                    if company_vals and not current_company:
                        company_vals.update({"is_company": True})
                        company = request.env["res.partner"].sudo().create(company_vals)
                        current_partner.sudo().write({"parent_id": company.id})
            else:

                print("====DEF=====")
                partner_id = request.env["res.partner"].sudo().create(partner_vals)

                if company_vals:
                    company_vals.update({"is_company": True})
                    company = request.env["res.partner"].sudo().create(company_vals)
                    partner_id.sudo().write({"parent_id": company.id})
                    company.sudo().write({"parent_id": order.partner_id.id})

                else:
                    partner_id.sudo().write({"parent_id": order.partner_id.id})

                order.sudo().write({"partner_invoice_id": partner_id})

            if current_user.partner_id == order.partner_id and not partner_id:
                if not order.use_different_billing_address:
                    order.sudo().write({"use_different_billing_address": True})
            if "submitted" in post and "editing" not in post:
                if not order.use_different_billing_address:
                    order.sudo().write({"use_different_billing_address": True})
            if current_partner == order.partner_id and partner_id and "submitted" in post:
                if not order.use_different_billing_address:
                    order.sudo().write({"use_different_billing_address": True})

            return request.redirect("/shop/extra_info")

        values = {
            "website_sale_order": order,
            "countries": countries,
            "order": order,
        }
        if "new_billing_address" in post:
            values.update({"partner": False})
        if (
            order.use_different_billing_address
            and order.partner_invoice_id != order.partner_id
            and "new_billing_address" not in post
        ):
            values.update({"partner": order.partner_invoice_id})

        if partner_id:
            print("===MENEE TANNE???===")
            edit_partner = (
                request.env["res.partner"].sudo().search([("id", "=", partner_id)])
            )
            if edit_partner in order.partner_id.child_ids or edit_partner == order.partner_invoice_id:
                values.update({"partner": edit_partner})
            else:
                # TAHAN JOKIN VIRHE ETTÄ EI MUUTEN ONNISTU
                return request.redirect("/shop/extra_info")

        return request.render("website_sale_billing_address.billing_address", values)
