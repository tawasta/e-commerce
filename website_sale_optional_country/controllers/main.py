from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleMandatoryZip(WebsiteSale):
    def _get_mandatory_billing_fields(self):
        res = super(WebsiteSaleMandatoryZip, self)._get_mandatory_billing_fields()

        if "country_id" in res:
            res.remove("country_id")

        return res

    def _get_mandatory_shipping_fields(self):
        res = super(WebsiteSaleMandatoryZip, self)._get_mandatory_shipping_fields()

        if "country_id" in res:
            res.remove("country_id")

        return res
