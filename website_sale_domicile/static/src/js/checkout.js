odoo.define("website_sale_domicile.checkout", function (require) {
    "use strict";
    var core = require("web.core");
    var _t = core._t;

    $(function () {
        $("input[name=city]").blur(function () {
            // Fill domicile after filling the city
            if (!$("input[name=domicile]").val()) {
                $("input[name=domicile]").val($("input[name=city]").val());
            }
        });
    });
});
