from odoo import http
from odoo.http import request
import logging
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleBilling(WebsiteSale):
    @http.route()
    def address(self, **kw):
        order = request.website.sale_get_order()

        if kw.get("billing_address"):
            custom_fields = {
                "company_email": kw.pop("company_email_billing", None),
                "company_registry": kw.pop("billing_company_registry", None),
                "customer_invoice_transmit_method_id": kw.pop(
                    "customer_invoice_transmit_method_id", None
                ),
            }

            # Email is a mandatory field
            kw["email"] = custom_fields["company_email"]

            response = super().address(**kw)
            if order.partner_invoice_id:
                partner_invoice = order.partner_invoice_id

                # Correct invoice address type
                update_values = {"type": "invoice"}

                if custom_fields.get("company_email"):
                    update_values["company_email"] = custom_fields["company_email"]

                    if hasattr(partner_invoice, "email_invoicing_address"):
                        update_values["email_invoicing_address"] = custom_fields[
                            "company_email"
                        ]

                if custom_fields.get("company_registry"):
                    update_values["company_registry"] = custom_fields[
                        "company_registry"
                    ]
                    update_values["vat"] = custom_fields["company_registry"]
                    update_values["is_company"] = True
                    update_values["company_type"] = "company"

                if custom_fields.get("customer_invoice_transmit_method_id"):
                    update_values["customer_invoice_transmit_method_id"] = int(
                        custom_fields["customer_invoice_transmit_method_id"]
                    )

                if update_values:
                    partner_invoice.sudo().write(update_values)
            else:
                logging.warning("Order does not have a partner_invoice_id!")

            return response

        if "submitted" in kw and request.httprequest.method == "POST":
            # Force checking your addresses
            kw["callback"] = "/shop/checkout"

        res = super().address(**kw)
        return res

    @http.route()
    def checkout(self, **post):
        res = super().checkout(**post)

        # Remove "mode"-parameter from first address screen
        order = request.website.sale_get_order()
        if order:
            partner_invoice = order.partner_invoice_id
            if not self._check_billing_partner_mandatory_fields(partner_invoice):
                # Return without "mode=billing"-parameter
                return request.redirect(
                    "/shop/address?partner_id=%d" % partner_invoice.id
                )

        return res
