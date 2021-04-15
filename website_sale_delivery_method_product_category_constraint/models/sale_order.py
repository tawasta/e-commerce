from odoo import models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def get_carriers(self, product_category):
        """A generator to check delivery methods"""
        for category_carrier in product_category.category_carrier:
            yield category_carrier

    def _get_delivery_methods(self):
        delivery_methods = super(SaleOrder, self)._get_delivery_methods()
        # lines is a generator object
        lines = (x for x in self.order_line if delivery_methods)
        for line in lines:
            # Skip a line if its product is the same as
            # sale order's delivery method's product
            if line.product_id == self.carrier_id.product_id:
                continue

            for delivery_method in delivery_methods:
                category = line.product_id.categ_id
                # Loop through all parent categories to check delivery methods
                while category:
                    carriers = self.get_carriers(category)
                    category = category.parent_id
                    # If all is fine, break the while-loop
                    if delivery_method in carriers:
                        break
                    else:
                        # Continue looping if category has a parent category
                        if category:
                            continue
                        # Else remove a delivery method
                        else:
                            delivery_methods -= delivery_method

        return delivery_methods
