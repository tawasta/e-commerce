# -*- coding: utf-8 -*-
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleOptionalAddress(WebsiteSale):

    def _get_mandatory_billing_fields(self):
        res = super(WebsiteSaleOptionalAddress,
                    self)._get_mandatory_billing_fields()

        if 'street' in res:
            res.remove('street')

        if 'city' in res:
            res.remove('city')

        if 'country_id' in res:
            res.remove('country_id')

        return res

    def _get_mandatory_shipping_fields(self):
        res = super(WebsiteSaleOptionalAddress,
                    self)._get_mandatory_shipping_fields()

        if 'street' in res:
            res.remove('street')

        if 'city' in res:
            res.remove('city')

        if 'country_id' in res:
            res.remove('country_id')

        return res
