from odoo import models
from odoo.http import request


class Website(models.Model):
    _inherit = "website"

    def _compute_checkout_skip_payment(self):
        for rec in self:
            if request.session.uid or request.env.user:
                rec.checkout_skip_payment = (
                    request.env.user.partner_id.skip_website_checkout_payment
                )
