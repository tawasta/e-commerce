odoo.define("website_sale_product_code.product", function (require) {
    "use strict";
    var ajax = require("web.ajax");

    $(function () {
        $(".product_id").change(function () {
            var product = parseInt($(this).val());
            var action = "/product/get/default_code";

            var values = {
                id: product,
            };

            ajax.jsonRpc(action, "call", values).then(function (code) {
                $(".product_code").text(code);
            });
        });
    });
});
