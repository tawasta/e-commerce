from odoo import models


class ResUsers(models.Model):
    _inherit = "res.users"

    def _is_partner_email_locked(self):
        """Whether the user's partner email follows their username, so it
        must not be changed in the checkout address form."""
        self.ensure_one()
        if not self._is_portal():
            return False
        # sudo: portal users cannot read system parameters
        return bool(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("website_portal_username_change.sync_partner_email")
        )
