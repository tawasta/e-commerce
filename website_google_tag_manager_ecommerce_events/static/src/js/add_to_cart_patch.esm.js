/** @odoo-module **/

import {WebsiteSale} from "@website_sale/js/website_sale";
import {patch} from "@web/core/utils/patch";
import {jsonrpc} from "@web/core/network/rpc_service";

patch(WebsiteSale.prototype, {
    async _onClickAdd(ev) {
        const result = await super._onClickAdd(...arguments);
        try {
            const form =
                ev.currentTarget.closest("form") ||
                document.querySelector("#product_detail form") ||
                document.querySelector("form.js_add_cart_variants");
            if (!form) return result;

            const productInput = form.querySelector('input[name="product_id"]');
            const qtyInput = form.querySelector('input[name="add_qty"]');
            const productId = productInput && parseInt(productInput.value);
            const qty = qtyInput ? parseFloat(qtyInput.value) : 1;
            if (!productId) return result;

            const payload = await jsonrpc("/shop/ga4/item", {
                product_id: productId,
                quantity: qty,
            });
            if (!payload || !payload.items) return result;

            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({ecommerce: null});
            window.dataLayer.push({
                event: "add_to_cart",
                ecommerce: payload,
            });
        } catch (err) {
            console.warn("GA4 add_to_cart push failed:", err);
        }
        return result;
    },
});
