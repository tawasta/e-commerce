##############################################################################
#
#    Author: Tawasta
#    Copyright 2018- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
    "name": "Website Sale Company Slider",
    "summary": "Slider to checkout",
    "version": "17.0.1.2.0",
    "category": "Website",
    "website": "https://gitlab.com/tawasta/odoo/e-commerce",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_sale",
        "website_sale_company_email",
        "website_sale_edicode",
    ],
    "data": [
        "data/config_parameter.xml",
        "views/product_template.xml",
        "views/website_sale_address.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_sale_company_slider/static/src/scss/style.scss",
            "website_sale_company_slider/static/src/js/checkout.esm.js",
        ],
    },
}
