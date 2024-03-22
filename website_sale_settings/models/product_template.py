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
import re

# 3. Odoo imports (openerp):
from odoo import models

# 2. Known third party imports:


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ProductTemplate(models.Model):
    # 1. Private attributes
    _inherit = "product.template"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    """
    :param combination: recordset of `product.template.attribute.value`

    :param int product_id: `product.product` id. If no `combination`
            is set, the method will try to load the variant `product_id` if
            it exists instead of finding a variant based on the combination.

            If there is no combination, that means we definitely want a
            variant and not something that will have no_variant set.

    :param float add_qty: the quantity for which to get the info,
            indeed some pricelist rules might depend on it.

    :param parent_combination: if no combination and no product_id are
            given, it will try to find the first possible combination, taking
            into account parent_combination (if set) for the exclusion rules.

    :param only_template: boolean, if set to True, get the info for the
            template only: ignore combination and don't try to find variant
    """

    def _get_combination_info(
        self,
        combination=False,
        product_id=False,
        add_qty=1,
        #pricelist=False, Poistunut 17 versiosta
        parent_combination=False,
        only_template=False,
    ):
        res = super(ProductTemplate, self)._get_combination_info(
            combination,
            product_id,
            add_qty,
            #pricelist, Poistunut 17 versiosta
            parent_combination,
            only_template,
        )
        display_name = res.get("display_name")
        # Regex pattern to remove all square brackets and contents inside
        pattern = r"\[[^\]]*\]"
        try:
            # Strip leading whitespace after regex
            name_without_code = re.sub(pattern, "", display_name).lstrip()
            res["name_without_code"] = name_without_code
        except TypeError:
            res["name_without_code"] = ""
        return res

    # 8. Business methods
