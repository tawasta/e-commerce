from odoo import http
from odoo import _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class CheckoutSkipPaymentAndConfirmation(WebsiteSale):

    @http.route()
    def payment_confirmation(self, **post):
        if not request.website.checkout_skip_payment:
            return super().payment_confirmation(**post)

        order = request.env['sale.order'].sudo().browse(
            request.session.get('sale_last_order_id'))

        # Mark SO as sent
        order.write({'state': 'sent'})

        # Add quotation print to message as an attachment
        attachment = request.env.ref(
            'sale.action_report_saleorder').sudo().render_qweb_pdf([order.id])
        attachment_name = _("Quotation {}").format(order.name)

        # Post an internal message to log
        order.message_post(
            subject=_("Order confirmed in website"),
            body=_("{} confirmed the order").format(request.env.user.name),
            attachments={(attachment_name, attachment[0])},
        )

        # The order is done
        request.website.sale_reset()
        return request.render("website_sale.confirmation", {'order': order})
