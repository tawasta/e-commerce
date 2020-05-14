from odoo import fields
from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    website_agent = fields.Boolean(
        string='Website Agent',
        help='This partner is a website agent, and will be able to select '
             'any address as delivery address, if the agent is the salesperson '
             'marked for the address',
    )
