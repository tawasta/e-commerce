from odoo import _, http
from odoo.http import request

from odoo.addons.website_sale_checkout_skip_payment.controllers.main import (
    CheckoutSkipPayment,
)


class CheckoutSkipPaymentAndConfirmation(CheckoutSkipPayment):
    @http.route()
    def payment_confirmation(self, **post):
        if not request.website.checkout_skip_payment:
            return super().payment_confirmation(**post)

        order = (
            request.env["sale.order"]
            .sudo()
            .browse(request.session.get("sale_last_order_id"))
        )

        commercial_partner = order.partner_id.commercial_partner_id

        # Change commercial partner to partner, if necessary
        if commercial_partner != order.partner_id:
            if hasattr(order, "customer_contact_id"):
                if not order.customer_contact_id:
                    order.customer_contact_id = order.partner_id.id

            order.partner_id = commercial_partner.id
            order.partner_invoice_id = commercial_partner.id

        # Mark SO as sent
        order.write({"state": "sent"})

        config = request.env["ir.config_parameter"].sudo()

        # Add quotation print to message as an attachment
        attachment = (
            request.env.ref("sale.action_report_saleorder")
            .sudo()
            ._render_qweb_pdf([order.id])
        )
        attachment_name = _("Quotation {}").format(order.name)

        if config.get_param("auto_send_quotation_from_ecommerce") == "1":
            order.force_quotation_send()
        else:
            # Post an internal message to log
            order.message_post(
                subject=_("Order confirmed in website"),
                body=_("{} confirmed the order").format(request.env.user.name),
                attachments={(attachment_name, attachment[0])},
            )

        # The order is done
        request.website.sale_reset()
        return request.render("website_sale.confirmation", {"order": order})
