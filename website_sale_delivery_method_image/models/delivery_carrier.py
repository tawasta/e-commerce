# -*- coding: utf-8 -*-


from odoo import fields, models


class DeliveryCarrier(models.Model):

    _inherit = 'delivery.carrier'

    delivery_image = fields.Binary(
        string="Delivery Image",
    )
