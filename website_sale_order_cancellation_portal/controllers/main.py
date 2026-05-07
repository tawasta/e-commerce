import logging

from markupsafe import Markup

from odoo import _, http
from odoo.http import request

from odoo.addons.sale.controllers.portal import CustomerPortal

_logger = logging.getLogger(__name__)


class SaleOrderCancellationPortal(CustomerPortal):
    @http.route(
        ["/my/orders/<int:order_id>/cancel"],
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
        csrf=True,
    )
    def portal_cancel_order(self, order_id, access_token=None, **post):
        try:
            order = self._document_check_access(
                "sale.order",
                order_id,
                access_token=access_token,
            )
        except Exception:
            return request.redirect("/my/orders?cancel_error=access")

        redirect_url = f"/my/orders/{order.id}"
        if access_token:
            redirect_url = f"{redirect_url}?access_token={access_token}"
            separator = "&"
        else:
            separator = "?"

        if not order.portal_cancellation_allowed:
            return request.redirect(
                f"{redirect_url}{separator}cancel_error=not_allowed"
            )

        if not post.get("confirm_cancellation"):
            return request.redirect(f"{redirect_url}{separator}cancel_error=confirm")

        reason = (post.get("cancellation_reason") or "").strip()

        try:
            cancellation = (
                request.env["sale.order.cancellation"]
                .sudo()
                .create(
                    {
                        "sale_order_id": order.id,
                        "cancellation_reason": reason or False,
                    }
                )
            )

            order.sudo().write({"portal_cancellation_received": True})

            body = Markup(
                """
                <p><strong>Customer submitted a cancellation notice.</strong></p>
                <ul>
                    <li><strong>Received at:</strong> {received_at}</li>
                    <li><strong>Reason:</strong> {reason}</li>
                </ul>
                """
            ).format(
                received_at=cancellation.received_at or "-",
                reason=reason or "-",
            )

            if order.invoice_ids:
                body += Markup(
                    """
                    <p>
                        <strong>Important:</strong>
                        This order has invoice(s). Possible refunds, credit
                        notes or accounting actions must be handled manually.
                    </p>
                    """
                )

            order.sudo().message_post(body=body)

            cancellation.sudo().message_post(
                body=_("Cancellation notice was received from the customer portal.")
            )

            customer_template = request.env.ref(
                "website_sale_order_cancellation_portal."
                "mail_template_customer_cancellation_confirmation",
                raise_if_not_found=False,
            )
            if customer_template:
                customer_template.sudo().send_mail(cancellation.id, force_send=True)

            manager_template = request.env.ref(
                "website_sale_order_cancellation_portal."
                "mail_template_manager_cancellation_alert",
                raise_if_not_found=False,
            )
            sales_manager_group = request.env.ref(
                "sales_team.group_sale_manager",
                raise_if_not_found=False,
            )

            users = sales_manager_group.users if sales_manager_group else order.user_id
            if not users:
                users = order.user_id

            activity_note = _(
                "Customer %(customer)s submitted a cancellation notice for "
                "order %(order)s."
            ) % {
                "customer": cancellation.partner_id.display_name,
                "order": order.name,
            }

            if order.invoice_ids:
                activity_note += _(
                    "\n\nThis order has invoice(s). Possible refunds, credit "
                    "notes or accounting actions must be handled manually."
                )

            for user in users:
                if manager_template and user.partner_id.email:
                    manager_template.sudo().send_mail(
                        cancellation.id,
                        force_send=True,
                        email_values={"email_to": user.partner_id.email},
                    )

                cancellation.sudo().activity_schedule(
                    "mail.mail_activity_data_todo",
                    user_id=user.id,
                    summary=_("New order cancellation notice"),
                    note=activity_note,
                )

            try:
                if order.state != "cancel":
                    order.sudo().with_context(
                        disable_cancel_warning=True
                    ).action_cancel()
            except Exception as e:
                _logger.warning(
                    "Automatic cancellation of sale order %s failed: %s",
                    order.name,
                    e,
                )
                order.sudo().message_post(
                    body=_(
                        "Automatic sale order cancellation failed after customer "
                        "submitted a cancellation notice. Please handle manually."
                    )
                )

        except Exception as e:
            _logger.exception("Portal order cancellation failed: %s", e)
            request.env.cr.rollback()
            return request.redirect(f"{redirect_url}{separator}cancel_error=1")

        return request.redirect(f"{redirect_url}{separator}cancel_ok=1")
