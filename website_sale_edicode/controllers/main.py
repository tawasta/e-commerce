from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def _checkout_form_save(self, mode, checkout, all_values):
        """
        Add edicode and operator to saved values
        """

        if all_values.get("edicode"):
            checkout["edicode"] = all_values.get("edicode")

        if all_values.get("einvoice_operator_id"):
            checkout["einvoice_operator_id"] = int(
                all_values.get("einvoice_operator_id")
            )

        return super()._checkout_form_save(mode, checkout, all_values)
