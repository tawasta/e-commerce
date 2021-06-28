from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleMandatoryCompany(WebsiteSale):
    def _get_mandatory_billing_fields(self):
        res = super()._get_mandatory_billing_fields()

        res.append("company_name")

        return res

    def _get_mandatory_shipping_fields(self):
        res = super()._get_mandatory_shipping_fields()

        # res.append("company_name")

        return res
