##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
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
    'name': 'eCommerce Quotations',
    'summary': 'Change the terminology used in eCommerce views',
    'version': '12.0.1.0.0',
    'category': 'Website',
    'website': 'https://github.com/Tawasta/e-commerce',
    'author': 'Oy Tawasta Technologies Ltd.',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'website_sale',
        'website_sale_no_payment_info',
    ],
    'data': [
        'views/website_sale_address.xml',
        'views/website_sale_cart.xml',
        'views/website_sale_cart_lines.xml',
        'views/website_sale_cart_popover.xml',
        'views/website_sale_checkout.xml',
        'views/website_sale_confirmation.xml',
        'views/website_sale_header.xml',
        'views/website_sale_product.xml',
        'views/website_sale_suggested_products_list.xml',
        'views/website_sale_wizard_checkout.xml',
    ],
}
