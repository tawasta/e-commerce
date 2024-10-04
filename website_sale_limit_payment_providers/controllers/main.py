from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSalePaymentProviders(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super()._get_shop_payment_values(order, **kwargs)

        # Haetaan kaikki maksupalveluntarjoajat ja maksutavat yhdellä kertaa suodatuksen helpottamiseksi
        payment_provider = request.env["payment.provider"].sudo()
        providers_sudo = values["providers_sudo"]
        filtered_providers_sudo = request.env["payment.provider"].sudo()

        # Hae kaikki sallitut maksupalveluntarjoajat yhdellä kyselyllä
        allowed_providers_set = set()
        for line in order.order_line:
            if line.product_id.allowed_payment_provider_ids:
                # Käytetään set-unionia, jotta vältetään saman palveluntarjoajan lisääminen useaan kertaan
                allowed_providers_set |= set(line.product_id.allowed_payment_provider_ids.ids)

        # Suodatus: poista providers, joita ei ole sallituissa
        if allowed_providers_set:
            filtered_providers_sudo = providers_sudo.filtered(lambda p: p.id in allowed_providers_set)

        # Käytä suodatettuja palveluntarjoajia, jos niitä löytyi
        if filtered_providers_sudo:
            providers_sudo = filtered_providers_sudo

        # Päivitä maksutavat vain, jos suodatettu lista poikkeaa alkuperäisestä
        if providers_sudo != values["providers_sudo"]:
            payment_method = request.env["payment.method"].sudo()

            payment_methods_sudo = payment_method._get_compatible_payment_methods(
                providers_sudo.ids,
                order.partner_id.id,
                currency_id=order.currency_id.id,
            )
            values["providers_sudo"] = providers_sudo
            values["payment_methods_sudo"] = payment_methods_sudo

        return values

