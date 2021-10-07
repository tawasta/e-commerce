from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def _checkout_form_save(self, mode, checkout, all_values):
        """
        Save company email to parent company
        """

        checkout["company_email"] = all_values.get("company_email", "")

        res = super(WebsiteSale, self)._checkout_form_save(mode, checkout, all_values)

        return res
