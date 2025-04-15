# models/product_template.py
from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval


class ProductTemplate(models.Model):
    _inherit = "product.template"

    paywall_domain = fields.Char(
        string="Paywall Domain",
        help="Comma-separated domain condition (safe_eval syntax) to show this product.",
    )

    user_in_paywall_domain = fields.Boolean(
        string="User has access to this product",
        compute="_compute_user_in_paywall_domain",
    )

    @api.depends("paywall_domain")
    def _compute_user_in_paywall_domain(self):
        partner = self.env["res.partner"].sudo()
        user_partner_id = self.env.user.partner_id.id
        for product in self:
            domain = False
            if product.paywall_domain:
                domain = [("id", "=", user_partner_id)] + safe_eval(
                    product.paywall_domain
                )
            product.user_in_paywall_domain = bool(domain and partner.search(domain))

    def _can_be_added_to_cart(self):
        res = super()._can_be_added_to_cart()
        if not res:
            return False
        return all(not p.paywall_domain or p.user_in_paywall_domain for p in self)
