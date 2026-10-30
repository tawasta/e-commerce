/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteSale.include({
    /**
     * Remove the country dialing code that core puts into the phone input
     * as a placeholder when the address country changes (website_sale.js
     * _changeCountry). This module has its own country code dropdown, so
     * that hint teaches customers to write "+358" into the phone field,
     * which is exactly the behavior the dropdown is meant to replace.
     */
    _changeCountry: async function () {
        await this._super(...arguments);
        for (const input of document.querySelectorAll("input[name='phone']")) {
            if ((input.getAttribute("placeholder") || "").startsWith("+")) {
                input.removeAttribute("placeholder");
            }
        }
    },
});
