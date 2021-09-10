from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    partner_id = fields.Many2one('res.partner', readonly=True, tracking=True,
            states={'draft': [('readonly', False)]},
            check_company=False,
            string='Partner', change_default=True)
