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
                order.sudo().write({"use_different_billing_address": True})

                return response
            else:
                return response
        else:
            return response

    # @http.route()
    # def confirm_order(self, **post):
    #     order = request.website.sale_get_order()
    #     if order.use_different_billing_address and order.par:
    #         return request.redirect("/shop/billing_address")
    #     else:
    #         return super(WebsiteSaleBilling, self).confirm_order(**post)

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
        if (
            order.use_different_billing_address
            and order.partner_id == order.partner_invoice_id
        ):
            order.sudo().write({"use_different_billing_address": False})
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

            if request.website.allow_selecting_sibling_billing_addresses:
                # Fetch sibling billing addresses, e.g. in this contact hierarchy:
                #
                # MainCompany
                # - MainCompany, Billing Address 1
                # - MainCompany, Billing Address 2
                # - MainCompany, Test Person 1
                #
                # ...Test Person 1, when in shop, would see also Billing Address 1 and 2
                if order.partner_id.parent_id and order.partner_id.parent_id.is_company:

                    sibling_billing_partners = (
                        request.env["res.partner"]
                        .sudo()
                        .search(
                            [
                                ("parent_id", "=", order.partner_id.parent_id.id),
                                ("type", "=", "invoice"),
                            ],
                            order="id desc",
                        )
                    )

                    billing_partners = billing_partners + sibling_billing_partners

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
        if not order:
            return request.redirect("/shop")
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
        Partner = request.env["res.partner"].sudo()
        order = request.website.sale_get_order()
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        countries = request.env["res.country"].sudo().search([])
        values = {
            "website_sale_order": order,
            "countries": countries,
            "order": order,
            "partner": False,
        }

        if "submitted" in post:
            partner_id = int(partner_id) if partner_id else None
            country_id = int(post.get("c_id", 0))
            einvoice_operator_id = post.get("einvoice_operator_id", 0)

            partner_vals = {
                "name": post.get("name"),
                "email": post.get("email"),
                "phone": post.get("phone"),
                "street": post.get("street"),
                "street2": post.get("street2"),
                "type": "invoice",
                "zip": post.get("zip"),
                "city": post.get("city"),
                "country_id": country_id,
                "business_code": post.get("vat"),
                # This will cause unexpected behaviour after confirming
                # "company_type": "company" if post.get("vat") else "person",
                "edicode": post.get("edicode"),
                "einvoice_operator_id": einvoice_operator_id or False,
                "customer_invoice_transmit_method_id": int(
                    post.get("customer_invoice_transmit_method_id", 0)
                )
                or False,
            }

            if hasattr(Partner, "email_invoicing_address"):
                partner_vals["email_invoicing_address"] = partner_vals.pop("email")

            if partner_id and "editing" in post:
                current_partner = Partner.browse(partner_id)
                if current_partner and current_partner != order.partner_id:
                    current_partner.write(partner_vals)
            else:
                new_partner = Partner.create(partner_vals)
                new_partner.parent_id = order.partner_id.id
                order.partner_invoice_id = new_partner
                order.use_different_billing_address = True

            return request.redirect("/shop/extra_info")

        # Load billing address info if user wants to edit or add new one
        if partner_id or "new_billing_address" in post:
            edit_partner = Partner.browse(partner_id) if partner_id else Partner
            if (
                edit_partner in order.partner_id.child_ids
                or edit_partner == order.partner_invoice_id
                or "new_billing_address" in post
            ):
                values["partner"] = edit_partner
            else:
                # Error handling: redirect if unauthorized edit attempt
                return request.redirect("/shop/extra_info")

        return request.render("website_sale_billing_address.billing_address", values)
