from odoo import fields, models


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _process_notification_data(self, notification_data):
        if self.provider_code == "custom" and self.provider_id.auto_confirm == "allow":
            # Auto-confirm SO if the payment provider is configured with auto-confirm
            self.sale_order_ids.action_confirm()

            # _set_pending() will not send confirmation mail if sale is already confirmed
            self.sale_order_ids._send_payment_succeeded_for_order_mail()

        return super()._process_notification_data(notification_data)
