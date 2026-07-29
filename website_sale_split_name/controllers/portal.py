import logging

from odoo.addons.portal.controllers.portal import CustomerPortal

logger = logging.getLogger(__name__)


class CustomerPortal(CustomerPortal):
    def _validate_address_values(
        self,
        address_values,
        partner_sudo,
        address_type,
        use_delivery_as_billing,
        required_fields,
        **kwargs,
    ):
        opt_view = (
            self.env["ir.ui.view"]
            .sudo()
            .with_context(active_test=False)
            .search(
                [
                    (
                        "key",
                        "=",
                        "website_sale_split_name._opt_split_name_in_website_sale_address_list",
                    )
                ],
                limit=1,
            )
        )
        if "firstname" in kwargs and "lastname" in kwargs and opt_view.active:
            firstname = kwargs["firstname"]
            lastname = kwargs["lastname"]
            address_values["firstname"] = firstname
            address_values["lastname"] = lastname
            address_values["name"] = f"{firstname} {lastname}"
        return super()._validate_address_values(
            address_values,
            partner_sudo,
            address_type,
            use_delivery_as_billing,
            required_fields,
            **kwargs,
        )

    def _get_mandatory_address_fields(self, country_sudo):
        result = super()._get_mandatory_address_fields(country_sudo)
        logger.error("HERE: ")
        opt_view = (
            self.env["ir.ui.view"]
            .sudo()
            .with_context(active_test=False)
            .search(
                [
                    (
                        "key",
                        "=",
                        "website_sale_split_name._opt_split_name_in_website_sale_address_list",
                    )
                ],
                limit=1,
            )
        )
        logger.error(opt_view)
        logger.error(opt_view.active)
        if opt_view.active:
            return result | set(["firstname", "lastname"])
        else:
            return result
