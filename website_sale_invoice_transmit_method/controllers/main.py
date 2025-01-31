from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def _checkout_form_save(self, mode, checkout, all_values):
        """
        Add invoice_transmit_method to saved values
        """
        if all_values.get("customer_invoice_transmit_method_id"):
            checkout["customer_invoice_transmit_method_id"] = int(
                all_values.get("customer_invoice_transmit_method_id")
            )

        return super()._checkout_form_save(mode, checkout, all_values)
