from odoo import fields
from odoo import models


class Website(models.Model):
    _inherit = 'website'

    add_explanation_text = fields.Html(string="Website sale: add an explanation", readonly=False, translate=True)

    add_attachment_text = fields.Html(string="Website sale: add an attachment", readonly=False, translate=True)

    product_categ_text = fields.Html(string="Website sale: Required product category text", readonly=False, translate=True)

    company_info_text = fields.Html(string="Website sale: need company data", readonly=False, translate=True)
