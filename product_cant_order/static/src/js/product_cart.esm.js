/** @odoo-module **/

import {WebsiteSale} from "@website_sale/js/website_sale";

WebsiteSale.include({
    _onChangeCombination: function (ev, $parent) {
        const res = this._super.apply(this, arguments);

        const productId = $parent.find(".product_id").val();
        const $addToCartButton = $parent.find("#add_to_cart");
        const $buyNowButton = $parent.find(".o_we_buy_now");

        const route = `/check/product/${productId}`;

        this.rpc(route).then(function (response) {
            if (response.can_not_order) {
                $addToCartButton.addClass("d-none");
                $buyNowButton.addClass("d-none");
            } else {
                $addToCartButton.removeClass("d-none");
                $buyNowButton.removeClass("d-none");
            }

            return res;
        });
    },
});

export default WebsiteSale;
