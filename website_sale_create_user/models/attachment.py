from odoo import api, models, fields


class IrAttachment(models.Model):

    _inherit = "ir.attachment"

    membership_attachment = fields.Boolean(string="Membership attachment")
