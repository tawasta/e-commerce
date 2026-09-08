from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    can_not_order_template = fields.Boolean(string="Cannot be Added to Cart")

    show_can_not_order_template = fields.Boolean(
        string="Show Template Can Not Order",
        compute="_compute_show_can_not_order_flags",
        store=False,
    )

    def _compute_show_can_not_order_flags(self):
        use_template = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("product_cant_order.can_not_order_use_template", "False")
            == "True"
        )
        for rec in self:
            rec.show_can_not_order_template = use_template


class ProductProduct(models.Model):
    _inherit = "product.product"

    can_not_order = fields.Boolean(string="Cannot be Added to Cart")

    show_can_not_order_variant = fields.Boolean(
        string="Show Variant Can Not Order",
        compute="_compute_show_can_not_order_flags",
        store=False,
    )

    def _compute_show_can_not_order_flags(self):
        use_template = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("product_cant_order.can_not_order_use_template", "False")
            == "True"
        )
        for rec in self:
            rec.show_can_not_order_variant = not use_template

    def get_effective_can_not_order(self):
        """
        Returns True if the product or its template is marked as
        'cannot be added to cart', depending on the configuration parameter
        'product_cant_order.can_not_order_use_template'.
        """
        self.ensure_one()
        use_template = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("product_cant_order.can_not_order_use_template", "False")
            == "True"
        )

        if use_template:
            return self.product_tmpl_id.can_not_order_template
        else:
            return self.can_not_order
