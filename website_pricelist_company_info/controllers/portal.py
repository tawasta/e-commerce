from odoo.addons.portal.controllers.portal import CustomerPortal


class Portal(CustomerPortal):
    def __init__(self):
        super().__init__()
        self.OPTIONAL_BILLING_FIELDS.extend(["property_product_pricelist"])

    def details_form_validate(self, data, partner_creation=False):
        error, error_message = super().details_form_validate(data, partner_creation)

        if data.get("property_product_pricelist"):
            data["property_product_pricelist"] = int(data["property_product_pricelist"])
        return error, error_message
