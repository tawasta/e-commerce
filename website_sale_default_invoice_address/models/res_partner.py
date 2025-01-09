from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    # prevent selecting invoice addresses that would raise
    # error 403 in website_sale's address()
    default_partner_invoice_id = fields.Many2one(
        domain="[('id', 'child_of', commercial_partner_id)]"
    )
