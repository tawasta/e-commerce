/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteSale.include({
    /**
     * Core triggers a change on the address country at page load
     * (website_sale.js start). Remember the rendered value so that event does
     * not overwrite the phone country rendered by the server, e.g. the
     * customer's own choice after a validation error.
     *
     * @override
     */
    start() {
        const addressCountry = this.el.querySelector("select[name='country_id']");
        this._phoneAddressCountryId = addressCountry && addressCountry.value;
        return this._super(...arguments);
    },

    _onChangeCountry() {
        this._syncPhoneCountry();
        return this._super(...arguments);
    },

    /**
     * Preselect a newly chosen address country as the phone country. Both
     * dropdowns use the res.country id as value. The customer can still pick
     * another country, e.g. for a foreign subscription.
     */
    _syncPhoneCountry() {
        const addressCountry = this.el.querySelector("select[name='country_id']");
        const phoneCountry = this.el.querySelector("select[name='phone_country_id']");
        if (
            !addressCountry ||
            !phoneCountry ||
            addressCountry.value === this._phoneAddressCountryId
        ) {
            return;
        }
        this._phoneAddressCountryId = addressCountry.value;
        // Countries without a dialing code have no option in the dropdown
        const hasOption = [...phoneCountry.options].some(
            (option) => option.value === addressCountry.value
        );
        phoneCountry.value = hasOption ? addressCountry.value : "";
    },

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
