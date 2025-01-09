##############################################################################
#
#    Author: Tawasta
#    Copyright 2020 Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

{
    "name": "Website sale billing address",
    "summary": "Website customer can select a billing address",
    "version": "17.0.1.0.3",
    "category": "Website",
    "website": "https://gitlab.com/tawasta/odoo/e-commerce",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_sale",
        "website_sale_invoice_transmit_method",
        "website_sale_split_name",
        "website_sale_domicile",
        "website_sale_company_email",
        "website_sale_default_privacies",
    ],
    "data": [
        "views/website_sale_address_kanban_template.xml",
        "views/website_sale_address_template.xml",
        "views/website_sale_checkout_template.xml",
        "views/website_sale_row_addresses_template.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_sale_billing_address/static/src/js/billing.esm.js",
        ],
    },
}
