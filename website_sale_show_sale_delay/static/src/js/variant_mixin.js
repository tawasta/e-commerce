odoo.define("website_sale_show_sale_delay.customVariantMixin", function (
    require
) {
    "use strict";

    var VariantMixin = require("website_sale_stock.VariantMixin");
    var publicWidget = require("web.public.widget");
    var ajax = require("web.ajax");
    var core = require("web.core");
    var QWeb = core.qweb;
    var xml_load = ajax.loadXML(
        "/website_sale_show_sale_delay/static/src/xml/websitesale_stock_product_availability.xml",
        QWeb
    );

    publicWidget.registry.WebsiteSale.include({
        _onChangeCombination: function (ev, $parent, combination) {
            this._super(ev, $parent, combination);
            this._customOnChangeCombinationStock(ev, $parent, combination);
        },

        _customOnChangeCombinationStock: function (ev, $parent, combination) {
            if (
                combination.product_type === "product" &&
                _.contains(["delivery_time"], combination.inventory_availability)
            ) {
                var qty = $parent.find('input[name="add_qty"]').val();
                $parent.find("#add_to_cart").removeClass("out_of_stock");
                $parent.find("#buy_now").removeClass("out_of_stock");
                combination.virtual_available -= parseInt(combination.cart_qty);
                // Combination.virtual_available -= parseInt(combination.cart_qty);
                if (combination.virtual_available < 0) {
                    combination.virtual_available = 0;
                }

                this._rpc({
                    route: "/get/more/info",
                    params: {
                        product_id: combination.product_template_id,
                    },
                }).then(function (results) {
                    combination.sale_delay = results.sale_delay;
                    if(combination.virtual_available == 0) {
                        $parent.find(".sale_delay").text(combination.sale_delay); 
                    }
                    
                });
            }
            xml_load.then(function () {
                $(".oe_website_sale")
                    .find(".availability_message_" + combination.product_template)
                    .remove();

                var $message = $(
                    QWeb.render(
                        "website_sale_show_sale_delay.product_availability",
                        combination
                    )
                );
                $("div.availability_messages").html($message);
            });
        },
    });

    return VariantMixin;
});
