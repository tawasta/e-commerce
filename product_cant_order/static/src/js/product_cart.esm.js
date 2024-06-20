/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.product_cant_order = publicWidget.Widget.extend({
    selector: "#product_details",

    events: {
        "change input.product_id": "_productIdChanged",
    },

    init: function () {
        this.rpc = this.bindService("rpc");
    },

    /**
     * When variant changes, check if the variant can be ordered.
     * If not, hide the add to cart button
     *
     */
    _productIdChanged: async function () {
        const productId = $("#product_details .js_main_product .product_id").val();
        const route = `/check/product/${productId}`;
        const $addToCartButton = $("#product_details #add_to_cart");

        const res = await this.rpc(route, {
            product_id: productId,
        });

        if (res.can_not_order) {
            $addToCartButton.addClass("d-none");
        } else {
            $addToCartButton.removeClass("d-none");
        }
    },
});
