odoo.define("website_sale_billing_address.billing_address", function () {
    "use strict";

    $(function () {
        $("#customer-invoice-transmit-method").on("change", function () {
            var method = $(this).val();
            if (method == "1") {
                $("#div_email").removeClass("d-none");
                $("#email_input").attr("required");
            } else {
                $("#div_email").addClass("d-none");
                $("#email_input").removeAttr("required");
            }
        });
    });
});
