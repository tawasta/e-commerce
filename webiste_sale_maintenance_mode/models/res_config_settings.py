# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval

from odoo import api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_sale_maintenance_mode = fields.Boolean(string='Website sale: Maintenance mode', config_parameter='website_sale.maintenance_mode', default=False)

    website_sale_maintenance_text = fields.Html(related='website_company_id.website_sale_maintenance_text', readonly=False)
