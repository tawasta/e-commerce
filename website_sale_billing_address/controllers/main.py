from odoo import http
from odoo.http import request
import logging
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleBilling(WebsiteSale):
    @http.route()
    def address(self, **kw):

        if kw.get('billing_address'):
        # Tallenna omat kentät ja poista ne kw:sta ennen superin kutsumista
            custom_fields = {
                'company_email': kw.pop('company_email_billing', None),
                'company_registry': kw.pop('billing_company_registry', None),
                'customer_invoice_transmit_method_id': kw.pop('customer_invoice_transmit_method_id', None)
            }
            # Kutsu alkuperäistä address-metodia ja lähetä loput kw-kentät
            response = super(WebsiteSaleBilling, self).address(**kw)

            # Tilauksen käsittely superin jälkeen
            order = request.website.sale_get_order()

            # Tarkistetaan, että orderilla on partner_invoice_id
            if order.partner_invoice_id:
                partner_invoice = order.partner_invoice_id

                # Päivitetään partner_invoice_id:n kentät, jos custom_fields sisältää arvoja
                update_values = {}
                
                if custom_fields.get('company_email'):
                    update_values['company_email'] = custom_fields['company_email']
                
                if custom_fields.get('company_registry'):
                    update_values['company_registry'] = custom_fields['company_registry']
                
                if custom_fields.get('customer_invoice_transmit_method_id'):
                    update_values['customer_invoice_transmit_method_id'] = int(custom_fields['customer_invoice_transmit_method_id'])
                
                # Jos päivitettäviä kenttiä on, tee päivitys
                if update_values:
                    logging.info(update_values);
                    partner_invoice.sudo().write(update_values)
                    logging.info(partner_invoice.company_registry);
                    logging.info(partner_invoice.company_email);
                    logging.info(partner_invoice.customer_invoice_transmit_method_id);
            else:
                logging.warning("Order does not have a partner_invoice_id!")

            return response
        else:
            return super(WebsiteSaleBilling, self).address(**kw)

