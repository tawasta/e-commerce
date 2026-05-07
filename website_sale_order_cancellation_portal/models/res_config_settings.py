from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    portal_cancellation_period_days = fields.Integer(
        string="Portal Cancellation Period in Days",
        default=14,
        config_parameter="website_sale_order_cancellation_portal.period_days",
    )