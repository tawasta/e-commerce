from odoo.addons.website_sale.controllers.product_configurator import (
    WebsiteSaleProductConfiguratorController,
)


class WebsiteSalePackagingConfiguratorController(
    WebsiteSaleProductConfiguratorController
):
    def _get_product_information(
        self, product_template, *args, product_uom_id=None, **kwargs
    ):
        # Core preselects the base UoM when none is given, which may not be
        # sold online. Outside eCommerce the first available UoM is the base UoM.
        product_uom_id = product_uom_id or product_template._get_available_uoms()[:1].id
        return super()._get_product_information(
            product_template, *args, product_uom_id=product_uom_id, **kwargs
        )
