from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleMandatoryZip(WebsiteSale):
    def _get_mandatory_billing_fields(self):
        res = super(WebsiteSaleMandatoryZip, self)._get_mandatory_billing_fields()

        if "city" in res:
            res.remove("city")

        return res

    def _get_mandatory_shipping_fields(self):
        res = super(WebsiteSaleMandatoryZip, self)._get_mandatory_shipping_fields()

        if "city" in res:
            res.remove("city")

        return res
