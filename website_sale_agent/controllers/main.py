from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request


class WebsiteSaleAddress(WebsiteSale):

    def values_postprocess(self, order, mode, values, errors, error_msg):
        new_values, errors, error_msg = \
            super(WebsiteSaleAddress, self).values_postprocess(
                order, mode, values, errors, error_msg)

        user = request.env.user

        if user.website_agent and 'parent_id' in new_values:
            # Remove parent (create a standalone shipping address)
            del(new_values['parent_id'])

            # Add as salesperson
            new_values['user_id'] = user.id

        return new_values, errors, error_msg

    def checkout_values(self, **kw):
        values = super(WebsiteSaleAddress, self).checkout_values(**kw)

        user = request.env.user

        if user.website_agent:
            # Website agents will see all delivery addresses where they are
            # marked as salesperson
            order = request.website.sale_get_order(force_create=1)

            # Change the order sale person
            order.user_id = user.id

            Partner = order.partner_id.with_context(show_address=1).sudo()
            shippings = Partner.search([
                ("user_id", "child_of", user.id),
                ("type", "in", ["delivery", "other"]),
            ], order='id desc')

            values['shippings'] = shippings

        return values
