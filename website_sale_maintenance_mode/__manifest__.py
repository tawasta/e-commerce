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
    "name": "Website Sale Maintenance mode",
    "summary": "Website Sale Maintenance mode",
    "version": "14.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/Tawasta/e-commerce",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_sale",
    ],
    "data": [
        "views/res_company_view.xml",
        "views/website_sale_template.xml",
        "views/res_config_settings_views.xml",
    ],
}
