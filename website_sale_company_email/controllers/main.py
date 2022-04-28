from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import tools, _


class WebsiteSale(WebsiteSale):
    def _checkout_form_save(self, mode, checkout, all_values):
        """
        Save company email to parent company
        """

        checkout["company_email"] = all_values.get("company_email", "")

        res = super(WebsiteSale, self)._checkout_form_save(mode, checkout, all_values)

        return res

    def checkout_form_validate(self, mode, all_form_values, data):
        error = {}
        error_message = []

        # company email validation
        if data.get('company_email') and not tools.single_email_re.match(data.get('company_email')):
            error["company_email"] = 'error'
            error_message.append(_('Invalid Company Email! Please enter a valid email address.'))

            return error, error_message

        return super(WebsiteSale, self).checkout_form_validate(
            mode, all_form_values, data
        )
