from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleAcquirers(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        res = super(WebsiteSaleAcquirers, self)._get_shop_payment_values(
            order, **kwargs
        )

        if order and res.get("acquirers"):
            print(order.partner_id)
            print(order.partner_id.is_company)
            print(order.partner_id.commercial_partner_id)
            print(order.partner_id.commercial_partner_id.is_company)
            print(order.partner_id.is_company or order.partner_id.is_company)
            if (
                order.partner_id.is_company
                or order.partner_id.commercial_partner_id.is_company
            ):
                acquirers = [
                    acq for acq in res["acquirers"] if acq.website_show_company
                ]
            else:
                acquirers = [
                    acq for acq in res["acquirers"] if acq.website_show_private
                ]

            res["acquirers"] = acquirers

        return res
