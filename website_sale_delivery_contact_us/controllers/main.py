from odoo.addons.website_sale_delivery.controllers.main import WebsiteSaleDelivery
from odoo import _


class WebsiteSaleDeliveryContact(WebsiteSaleDelivery):
    def _get_shop_payment_values(self, order, **kwargs):
        values = super(WebsiteSaleDeliveryContact, self)._get_shop_payment_values(
            order, **kwargs
        )

        has_storable_products = any(
            line.product_id.type in ["consu", "product"] for line in order.order_line
        )

        if has_storable_products:
            if len(values["errors"]) <= 1:
                contact_link = (
                    "<a href='/contactus?"
                    "contact_name={contact_name}"
                    "&phone={phone}"
                    "&email_from={email_from}"
                    "&partner_name={partner_name}"
                    "&name={name}"
                    "&description={description}"
                    "'>{text}</a>".format(
                        contact_name=order.partner_id.name,
                        phone=order.partner_id.phone or "-",
                        email_from=order.partner_id.email or "-",
                        partner_name=order.partner_id.company_name or "-",
                        name=_("Delivery of order {}").format(order.name),
                        description=_(
                            "There were no suitable delivery options for my order {}. Please advise"
                        ).format(order.name),
                        text=_("Contact us here for more delivery options"),
                    )
                )

                values["contact_us"] = contact_link

        return values
