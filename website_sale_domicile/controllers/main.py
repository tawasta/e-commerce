from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleDomicile(WebsiteSale):
    def _checkout_form_save(self, mode, checkout, all_values):
        """
        Add domicile to saved values
        """
        checkout["domicile"] = all_values.get("domicile") or False

        return super()._checkout_form_save(mode, checkout, all_values)
