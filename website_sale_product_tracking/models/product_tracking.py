from odoo import models, fields, api
import logging

class ProductTracking(models.Model):
    _name = 'product.tracking'
    _description = 'Product Tracking'

    product_id = fields.Many2one('product.product', string='Product')
    is_available = fields.Boolean(string='Is Available', compute='_compute_available_in_stock', default=False)
    email = fields.Char(string='Customer')

    @api.depends('product_id')
    def _compute_available_in_stock(self):
        for tracking in self:
            product = tracking.product_id
            quants = self.env['stock.quant'].search([
                ('product_id', '=', product.id),
                ('location_id.usage', '=', 'internal')
            ])
            total_quantity = sum(quant.quantity for quant in quants)
            tracking.is_available = total_quantity > 0

            # if tracking.is_available:
            #     # Lähetä sähköposti, jos is_available on True
            #     mail_values = {
            #         'subject': 'Tuote on nyt saatavilla',
            #         'body_html': '<h1>Tuote on nyt saatavilla</h1>',
            #         'email_from': self.env.user.email_formatted,
            #         'email_to': tracking.email,
            #     }
                
            #     self.env['mail.mail'].create(mail_values).send()

            #     # Poista rekordi
            #     tracking.unlink()
            # else:
            #     tracking.is_available = False
                

