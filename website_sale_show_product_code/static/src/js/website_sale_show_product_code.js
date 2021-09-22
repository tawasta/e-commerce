odoo.define(
    "website_sale_show_product_code.website_sale_show_product_code",
    function (require) {
        "use strict";
        var ajax = require("web.ajax");

        $(document).ready(function () {
            $("#product_id-id")
                .change(function () {
                    // When attribute selections change, find the variant that
                    // matches the selected attributes
                    var variant_id = $("#product_id-id");
                    var default_code_selector = ".product-variant-default-code";
                    if (variant_id[0]) {
                        // If a variant exists for the attribute combination,
                        // query its internal reference from the backend
                        ajax.jsonRpc("/shop/get_variant_code/", "call", {
                            product_id: variant_id[0].value,
                        }).then(function (data) {
                            $(default_code_selector).text(data.code);
                        });
                    } else {
                        // If an impossible attribute combination was selected,
                        // clear the shown internal reference
                        $(default_code_selector).text("-");
                    }
                    // Trigger after being bound so that the code shows up also after
                    // the product page initally loads.
                })
                .change();
        });
    }
);
