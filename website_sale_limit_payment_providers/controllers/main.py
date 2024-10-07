from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSalePaymentProviders(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super()._get_shop_payment_values(order, **kwargs)

        # Haetaan kaikki maksupalveluntarjoajat ja maksutavat yhdellä kertaa suodatuksen helpottamiseksi
        providers_sudo = values["providers_sudo"]
        filtered_providers_sudo = request.env["payment.provider"].sudo()

        # Hae kaikki sallitut maksupalveluntarjoajat yhdellä kyselyllä
        allowed_providers_list = []
        for line in order.order_line:
            if line.product_id.allowed_payment_provider_ids:
                allowed_providers_list.append(
                    set(line.product_id.allowed_payment_provider_ids.ids)
                )

        # Tarkistetaan, onko olemassa ristiriitaisia maksupalveluntarjoajia
        if allowed_providers_list:
            common_providers = set.intersection(*allowed_providers_list)
            if not common_providers:
                # Jos ristiriita löytyy, tyhjennetään maksupalveluntarjoajat
                values["providers_sudo"] = request.env["payment.provider"].sudo()
                values["payment_methods_sudo"] = request.env["payment.method"].sudo()
                return values
            else:
                # Suodatus: käytetään vain yhteisiä maksupalveluntarjoajia
                filtered_providers_sudo = providers_sudo.filtered(
                    lambda p: p.id in common_providers
                )

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
