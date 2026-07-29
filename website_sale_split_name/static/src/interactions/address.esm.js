import {CustomerAddress} from "@portal/interactions/address";
import {patch} from "@web/core/utils/patch";

patch(CustomerAddress.prototype, {
  _markRequired(name, required) {
    const input = this.addressForm[name];
    if (input) {
      /* For some reason a string is being passed here, so check for object
       * This if clause is only change from original v19 version
       * 2026-07-28
       * https://github.com/odoo/odoo/blob/1b695c64a71df8316dc0d841b4452f6be9eac061/addons/portal/static/src/interactions/address.js#L122
       */
      if (typeof input === "object") {
        input.required = required;
        this._getInputLabel(name)?.classList.toggle("label-optional", !required);
      }
    }
  },
});
