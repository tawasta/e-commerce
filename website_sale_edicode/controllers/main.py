from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def _checkout_form_save(self, mode, checkout, all_values):
        """
        Add edicode and operator to saved values
        """
        checkout["edicode"] = all_values.get("edicode", "")
        checkout["einvoice_operator"] = all_values.get("einvoice_operator", "")
        return super(WebsiteSale, self)._checkout_form_save(mode, checkout, all_values)
