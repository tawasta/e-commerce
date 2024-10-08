/** @odoo-module **/

import {WebsiteSale} from "@website_sale/js/website_sale";

WebsiteSale.include({
    _onChangeCombination: function (ev, $parent) {
        const res = this._super.apply(this, arguments);

        const productId = $parent.find(".product_id").val();
        const route = "/shop/get_variant_code/";
        const default_code_selector = ".product-variant-default-code";

        // When attribute selections change, find the variant that
        // matches the selected attributes

        this.rpc(route, {product_id: productId}).then(function (response) {
            $(default_code_selector).text(response.code);

            return res;
        });
    },
});

export default WebsiteSale;
