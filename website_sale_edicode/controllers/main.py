from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def _checkout_form_save(self, mode, checkout, all_values):
        """
        Add edicode and operator to saved values
        """
        checkout["edicode"] = all_values.get("edicode") or False
        checkout["einvoice_operator_id"] = (
            all_values.get("einvoice_operator_id") or False
        )
        return super(WebsiteSale, self)._checkout_form_save(mode, checkout, all_values)
