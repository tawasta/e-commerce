from odoo import http
from odoo.http import request
import logging
from odoo import fields, http, SUPERUSER_ID, tools, _
from werkzeug.exceptions import Forbidden, NotFound
from odoo.exceptions import ValidationError
from odoo.osv import expression

from odoo.addons.website_sale_split_name.controllers.main import WebsiteSale


class CustomWebsiteSale(WebsiteSale):


    def _get_mandatory_shipping_fields(self):
        # Remove 'firstname' and 'lastname' from mandatory fields for shipping
        fields = super(CustomWebsiteSale, self)._get_mandatory_shipping_fields()
        fields.remove('firstname')
        fields.remove('lastname')
        logging.info("====FIELDS====");
        logging.info(fields);
        return fields

    @http.route()
    def address(self, **kw):
        logging.info(kw);
        if "submitted" in kw:
            if "name" in kw and kw.get("name"):
                logging.info("==ONKO TAMA====");
                kw["name"] = kw.get("name")
            else:
                logging.info("===VAI TAMA====");
                name = request.env["res.partner"]._get_computed_name(
                    kw.get("lastname"), kw.get("firstname")
                )
                kw["name"] = name
        logging.info(kw);

        return super(CustomWebsiteSale, self).address(**kw)

    def checkout_form_validate(self, mode, all_form_values, data):
        logging.info(all_form_values);
        logging.info(data);
        # mode: tuple ('new|edit', 'billing|shipping')
        # all_form_values: all values before preprocess
        # data: values after preprocess
        error = dict()
        error_message = []

        # prevent name change if invoices exist
        if data.get('partner_id'):
            partner = request.env['res.partner'].browse(int(data['partner_id']))
            if partner.exists() and partner.name and not partner.sudo().can_edit_vat() and 'name' in data and (data['name'] or False) != (partner.name or False):
                error['name'] = 'error'
                error_message.append(_('Changing your name is not allowed once invoices have been issued for your account. Please contact us directly for this operation.'))

        # Required fields from form
        required_fields = [f for f in (all_form_values.get('field_required') or '').split(',') if f]

        # Required fields from mandatory field function
        country_id = int(data.get('country_id', False))
        required_fields += mode[1] == 'shipping' and self._get_mandatory_fields_shipping(country_id) or self._get_mandatory_fields_billing(country_id)
        logging.info("===REQ======");
        logging.info(required_fields);
        # error message for empty required fields
        for field_name in required_fields:
            if not data.get(field_name):
                logging.info(field_name);
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        Partner = request.env['res.partner']
        if data.get("vat") and hasattr(Partner, "check_vat"):
            if country_id:
                data["vat"] = Partner.fix_eu_vat_number(country_id, data.get("vat"))
            partner_dummy = Partner.new(self._get_vat_validation_fields(data))
            try:
                partner_dummy.check_vat()
            except ValidationError as exception:
                error["vat"] = 'error'
                error_message.append(exception.args[0])

        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        return error, error_message
