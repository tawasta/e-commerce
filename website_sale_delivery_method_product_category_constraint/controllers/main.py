from odoo.addons.website_sale_delivery.controllers.main import WebsiteSaleDelivery


class WebsiteSaleDelivery(WebsiteSaleDelivery):

    def get_carriers(self, product_category_carrier):
        """A generator to check delivery methods"""
        for category_carrier in product_category_carrier:
            yield category_carrier.carrier

    def _get_shop_payment_values(self, order, **kwargs):
        values = super(WebsiteSaleDelivery, self)._get_shop_payment_values(
            order, **kwargs)
        delivery_methods = order._get_delivery_methods()
        # lines is a generator object
        lines = (x for x in order.order_line if order and delivery_methods)
        for line in lines:
            # Skip a line if its product is the same as
            # sale order's delivery method's product
            if line.product_id == order.carrier_id.product_id:
                continue

            for delivery_method in delivery_methods:
                category = line.product_id.categ_id
                # Loop through all parent categories to check delivery methods
                while category:
                    carriers = self.get_carriers(category.category_carrier)
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

        values['deliveries'] = delivery_methods.sudo() or False
        return values
