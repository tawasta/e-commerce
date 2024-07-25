from odoo import fields, models, api, _lt


class Website(models.Model):
    _inherit = "website"

    # allow_selecting_sibling_billing_addresses = fields.Boolean(
    #     string="Allow Selecting Sibling Billing Addresses",
    #     default=False,
    #     help="Let the customer select also from those billing addressed that are not "
    #     "directly linked to the customer but belong to the same parent company.",
    # )

    @api.model
    def _get_checkout_steps(self, current_step=None):
        steps = super(Website, self)._get_checkout_steps(current_step)

        billing_step = (
            ["website_sale_billing_address.billing_address"],
            {
                "name": _lt("Billing Address"),
                "current_href": "/shop/billing_address",
                "main_button": _lt("Next"),
                "main_button_href": "/shop/extra_info",
                "back_button": _lt("Back to shipping"),
                "back_button_href": "/shop/checkout",
            },
        )

        for index, step in enumerate(steps):
            if "website_sale.address" in step[0]:
                steps.insert(index + 1, billing_step)
                break

        return steps
