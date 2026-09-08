/** @odoo-module **/

import {rpc} from "@web/core/network/rpc";
import {patch} from "@web/core/utils/patch";
import {WebsiteSale} from "@website_sale/interactions/website_sale";

patch(WebsiteSale.prototype, {
  async _onChangeCombination(ev, parent) {
    await super._onChangeCombination(...arguments);

    const productId = parseInt(parent.querySelector(".product_id")?.value);
    if (!productId) {
      return;
    }

    const route = `/check/product/${productId}`;
    const response = await this.waitFor(rpc(route));

    parent
      .querySelector("#add_to_cart")
      ?.classList.toggle("d-none", response.can_not_order);
    parent
      .querySelector(".o_we_buy_now")
      ?.classList.toggle("d-none", response.can_not_order);
  },
});
