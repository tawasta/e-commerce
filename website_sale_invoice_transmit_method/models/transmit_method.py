# Copyright 2017-2020 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class TransmitMethod(models.Model):
    _inherit = "transmit.method"

    website_sale_ok = fields.Boolean(string="Selectable on e-commerce", default=False)
