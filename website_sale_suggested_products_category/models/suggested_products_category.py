##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
from odoo import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SuggestedProductsCategory(models.Model):
    # 1. Private attributes
    _name = "suggested.products.category"
    _inherit = [
        "website.multi.mixin",
    ]
    _description = "Suggested Accessory Products Category"
    _order = "sequence, name, id"

    # 2. Fields declaration
    name = fields.Char(
        "Suggested Accessory Products Category", required=True, translate=True
    )
    sequence = fields.Integer("Sequence", default=1)
    description = fields.Text(
        "Description",
        required=True,
        translate=True,
        help="Description displayed for the suggested accessory products "
        "category on the website.",
    )
    product_public_category_ids = fields.One2many(
        comodel_name="product.public.category",
        inverse_name="suggested_products_category_id",
        string="eCommerce Categories",
        help="Products from these eCommerce Categories will be included under this "
        "Suggested Accessory Products Category.",
    )
    product_ids = fields.Many2many(
        "product.product", "Products", compute="_compute_product_ids"
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _compute_product_ids(self):
        for rec in self:
            products = self.env["product.product"].search(
                [["public_categ_ids", "in", rec.product_public_category_ids.ids]]
            )
            rec.product_ids = products

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
