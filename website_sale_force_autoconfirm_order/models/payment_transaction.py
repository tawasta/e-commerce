##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
import logging

# 3. Odoo imports (openerp):
from odoo import models
from odoo.tools import float_compare

# 2. Known third party imports:


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    # 1. Private attributes
    _inherit = "payment.transaction"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def _confirm_so(self, acquirer_name=False):
        # Do the core checks first whether the related SO should get
        # confirmed. Afterwards check if the acquirer has the new force confirm
        # mode selected. If yes, confirm the order.

        res = super(PaymentTransaction, self)._confirm_so(acquirer_name)

        for tx in self:
            if tx.sale_order_id and tx.sale_order_id.state in ["draft", "sent"]:
                amount_matches = (
                    float_compare(tx.amount, tx.sale_order_id.amount_total, 2) == 0
                )
                if amount_matches:
                    if not acquirer_name:
                        acquirer_name = tx.acquirer_id.provider or "unknown"
                    if tx.acquirer_id.auto_confirm == "force_confirm":
                        _logger.info(
                            "<%s> force confirming order %s (ID %s)",
                            acquirer_name,
                            tx.sale_order_id.name,
                            tx.sale_order_id.id,
                        )

                        tx.sale_order_id.with_context(send_email=True).action_confirm()

        return res

    # 8. Business methodsfrom odoo import models
