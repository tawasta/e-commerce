from odoo import _
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSalePartnerEmailReadonly(WebsiteSale):
    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super().checkout_form_validate(
            mode, all_form_values, data
        )
        # The form field is read-only, this stops a hand-crafted request
        if self._is_locked_email_changed(all_form_values, data):
            error["email"] = "error"
            error_message.append(
                _(
                    "Your email address follows your username "
                    "and cannot be changed here."
                )
            )
        return error, error_message

    def _create_or_edit_partner(self, partner_details, edit=False, **custom_values):
        # The express checkout routes are public and always registered, even
        # without an express payment method, and they edit the partner without
        # checkout_form_validate. The email is dropped instead of refused so
        # that a legitimate express checkout still continues.
        if edit and self._is_own_locked_partner(custom_values.get("partner_id")):
            partner_details = dict(partner_details)
            partner_details.pop("email", None)
        return super()._create_or_edit_partner(
            partner_details, edit=edit, **custom_values
        )

    def _is_locked_email_changed(self, all_form_values, data):
        # Core picks the edited partner from the same form value
        partner_id = int(all_form_values.get("partner_id") or -1)
        if not self._is_own_locked_partner(partner_id):
            return False
        partner = request.env.user.partner_id
        return (data.get("email") or "") != (partner.email or "")

    def _is_own_locked_partner(self, partner_id):
        user = request.env.user
        return partner_id == user.partner_id.id and user._is_partner_email_locked()
