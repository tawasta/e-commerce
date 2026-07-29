from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):
    def _parse_form_data(self, form_data):
        address_values, extra_form_data = super()._parse_form_data(form_data)
        if "domicile" in extra_form_data:
            address_values["domicile"] = extra_form_data.pop("domicile")
        return address_values, extra_form_data
