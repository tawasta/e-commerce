from odoo import models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _cart_add(self, product_id, quantity=1.0, *, uom_id=None, **kwargs):
        if kwargs.get("combo_item_id"):
            # The combo item price ignores the UoM: never trust one from the
            # browser, core then uses the base UoM
            uom_id = None
        elif not uom_id:
            # Core falls back to the base UoM, which may not be sold online
            product = self.env["product.product"].browse(product_id)
            uom_id = product.product_tmpl_id._get_available_uoms()[:1].id
        return super()._cart_add(product_id, quantity, uom_id=uom_id, **kwargs)

    def _check_cart_is_ready_to_be_paid(self):
        # `_cart_add` validates new lines only. Lines added before the
        # restriction or merged from an abandoned cart are checked here.
        lines = self.order_line.filtered(
            lambda line: line.product_id and not line.combo_item_id
        )
        for line in lines:
            website_uoms = line.product_template_id._get_website_uoms()
            if website_uoms and line.product_uom_id not in website_uoms:
                raise ValidationError(
                    self.env._(
                        "%(product)s cannot be bought in %(uom)s. Please remove "
                        "it from your cart and add it again.",
                        product=line.product_id.display_name,
                        uom=line.product_uom_id.name,
                    )
                )
        return super()._check_cart_is_ready_to_be_paid()
