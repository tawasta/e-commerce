from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.http import request


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Explicit relation: the default table name is already taken by `uom_ids`
    website_uom_ids = fields.Many2many(
        comodel_name="uom.uom",
        relation="product_template_website_uom_rel",
        column1="product_tmpl_id",
        column2="uom_id",
        string="eCommerce Packagings",
        help="Units and packagings in which this product can be bought on "
        "eCommerce. Leave empty to allow all of them.",
    )

    @api.constrains("uom_id", "uom_ids", "website_uom_ids")
    def _check_website_uom_ids(self):
        # A packaging outside the product's own would silently lift the restriction
        for template in self:
            if template.website_uom_ids - template.uom_id - template.uom_ids:
                raise ValidationError(
                    self.env._(
                        "The eCommerce packagings of %(product)s must be its "
                        "unit or one of its packagings.",
                        product=template.display_name,
                    )
                )

    def _get_website_uoms(self):
        """Return the UoMs allowed on eCommerce, or an empty recordset when
        the product is not restricted in the current request."""
        self.ensure_one()
        if not (request and request.is_frontend) or not self.website_uom_ids:
            return self.env["uom.uom"]
        if self.type == "combo" or not self.env["res.groups"]._is_feature_enabled(
            "uom.group_uom"
        ):
            return self.env["uom.uom"]
        # Intersection keeps the core order: base unit first, then packagings
        return super()._get_available_uoms() & self.website_uom_ids

    def _get_available_uoms(self):
        return self._get_website_uoms() or super()._get_available_uoms()

    def _has_multiple_uoms(self):
        # Show the packaging selector and the cart UoM label also when only
        # one packaging is allowed, so the customer sees what is bought. This
        # also makes core `_cart_add` validate the requested UoM.
        return super()._has_multiple_uoms() or bool(self._get_website_uoms())

    def _get_combination_info(
        self,
        combination=False,
        product_id=False,
        add_qty=1.0,
        uom_id=False,
        only_template=False,
    ):
        # Core prices the base UoM when none is given, which may not be sold
        uom_id = uom_id or self._get_available_uoms()[:1].id
        return super()._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            uom_id=uom_id,
            only_template=only_template,
        )

    def _get_sales_prices(self, website):
        prices = super()._get_sales_prices(website)
        # Core shop grid would always show the base UoM price
        for template in self:
            uom = template._get_website_uoms()[:1]
            if uom and uom != template.uom_id:
                # Update in place to keep keys added by other modules
                template_prices = prices[template.id]
                template_prices.pop("base_price", None)
                template_prices.update(template._prepare_website_uom_price_vals(uom))
        return prices

    def _prepare_website_uom_price_vals(self, uom):
        """Return shop grid price values for one unit of the given UoM, in the
        same format as core `_get_sales_prices`."""
        self.ensure_one()
        info = self._get_combination_info(only_template=True, uom_id=uom.id)
        price_vals = {"price_reduce": info["price"]}
        if info["has_discounted_price"]:
            price_vals["base_price"] = info["list_price"]
        elif info.get("compare_list_price"):
            price_vals["base_price"] = info["compare_list_price"]
        return price_vals
