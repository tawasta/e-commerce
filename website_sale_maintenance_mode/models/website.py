from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    def _maintenance_mode(self):
        # If maintenance mode is set, and user doesn't belong to website editors
        get_param = self.env["ir.config_parameter"].sudo().get_param
        maintenance_mode = get_param("website_sale.maintenance_mode")

        return maintenance_mode == "True" and not self.env.user.has_group(
            "website.group_website_designer"
        )
