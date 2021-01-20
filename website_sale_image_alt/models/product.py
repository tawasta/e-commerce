##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2019- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, models, fields

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ProductImage(models.Model):

    # 1. Private attributes
    _inherit = "product.image"

    # 2. Fields declaration
    alt = fields.Char(
        string="Alt", default=lambda self: self._get_default_alt(), required=True,
    )

    # 3. Default methods
    @api.model
    def _get_default_alt(self):
        return self.env["product.template"].name

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges
    @api.onchange("name")
    def image_name_change(self):
        if not self.alt:
            self.alt = self.name

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods


class ProductTemplate(models.Model):

    # 1. Private attributes
    _inherit = "product.template"

    # 2. Fields declaration
    alt = fields.Char(
        string="Main Image Alt", default=lambda self: self._get_default_alt(),
    )

    # 3. Default methods
    @api.model
    def _get_default_alt(self):
        return self.env["product.template"].name

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges
    @api.onchange("name")
    def image_name_change(self):
        if not self.alt:
            self.alt = self.name

    # 6. CRUD methods
    # @api.model
    # def create(self, vals):
    #     res = super(ProductTemplate, self).create(vals)
    #     print(res)
    #     # if not self.product_image_alt:
    #     #     self.product_image_alt = self.name
    #     return res

    # @api.multi
    # def write(self, vals):
    #     res = super(ProductTemplate, self).write(vals)
    #     if not self.product_image_alt:
    #         self.product_image_alt = self.name
        # return res

    # 7. Action methods

    # 8. Business methods
