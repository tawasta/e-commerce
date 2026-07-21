##############################################################################
#
#    Author: Futural Oy
#    Copyright 2018 Futural Oy (https://futural.fi)
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
    "name": "Website Sale Account Invoice Transmit Method",
    "summary": "Adds account invoice transmit method to checkout",
    "version": "19.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/tawasta/e-commerce",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "account_invoice_transmit_method",
        "website_sale",
    ],
    "data": [
        "views/transmit_method.xml",
        "views/website_template_checkout.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_sale_invoice_transmit_method/static/src/js/checkout.esm.js",
        ],
    },
    "demo": [],
}
