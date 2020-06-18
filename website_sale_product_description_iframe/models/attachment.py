from odoo import fields
from odoo import models


class Attachment(models.Model):

    _inherit = "ir.attachment"

    iframe_url = fields.Char(
        string='iframe URL',
        compute='_compute_iframe_url',
    )

    def _compute_iframe_url(self):
        for record in self:
            url = '<iframe class="col-12" src={}></iframe>'.format(
                record.website_url
            )

            record.iframe_url = url
