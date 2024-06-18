/** @odoo-module **/

import {WebsiteSale} from "@website_sale/js/website_sale";

WebsiteSale.include({
    events: Object.assign({}, WebsiteSale.prototype.events, {
        'change input[name="city"]': "_onChangeCity",
    }),

    /**
     * @private
     * @returns {Domicile} Domicile based on City.
     */
    _onChangeCity: function () {
        return this._changeCity();
    },

    _changeCity: function () {
        // Fill domicile after filling the city
        if (!$("input[name=domicile]").val()) {
            $("input[name=domicile]").val($("input[name=city]").val());
        }
    },
});

export default WebsiteSale;
