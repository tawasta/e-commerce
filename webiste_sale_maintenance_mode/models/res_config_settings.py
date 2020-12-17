from odoo import fields
from odoo import models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_sale_maintenance_mode = fields.Boolean(string='Website sale: Maintenance mode', config_parameter='website_sale.maintenance_mode', default=False)
    website_sale_maintenance_text = fields.Html(related='website_company_id.website_sale_maintenance_text', readonly=False)
