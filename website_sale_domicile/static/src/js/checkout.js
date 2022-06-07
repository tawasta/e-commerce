odoo.define("website_sale_domicile.checkout", function () {
    "use strict";

    $(function () {
        $("input[name=city]").blur(function () {
            // Fill domicile after filling the city
            if (!$("input[name=domicile]").val()) {
                $("input[name=domicile]").val($("input[name=city]").val());
            }
        });
    });
});
