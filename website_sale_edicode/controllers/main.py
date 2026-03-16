from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):
    def _create_or_update_address(
        self,
        partner_sudo,
        address_type="billing",
        use_delivery_as_billing=False,
        callback="/my/addresses",
        required_fields=False,
        verify_address_values=True,
        **form_data,
    ):
        if "edicode" in form_data:
            partner_sudo.edicode = form_data["edicode"]
        if "einvoice_operator_id" in form_data:
            einvoice_operator = (
                self.env["res.partner.operator.einvoice"]
                .sudo()
                .search([("id", "=", form_data["einvoice_operator_id"])], limit=1)
            )
            partner_sudo.einvoice_operator_id = einvoice_operator

        return super()._create_or_update_address(
            partner_sudo,
            address_type="billing",
            use_delivery_as_billing=False,
            callback="/my/addresses",
            required_fields=False,
            verify_address_values=True,
            **form_data,
        )
