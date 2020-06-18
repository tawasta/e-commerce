from odoo import fields
from odoo import models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    website_description_iframe_html = fields.Many2one(
        comodel_name='ir.attachment',
        string='HTML description',
        help='HTML file for description',
        domain=[('res_model', '=', 'product.template')]
    )
