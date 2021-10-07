odoo.define("website_sale_edicode.checkout", function (require) {
    "use strict";

    $(function () {
        $("#einvoice-operator-select").select2({
            allowClear: true,
        });

        function toggleEdicode() {
            var company = $("input[name=company_name]").val().length != 0;
            var speed = "slow";

            if (company) {
                $("#einvoice-operator-div").fadeIn();
                $("#edicode-div").fadeIn();
                $("#edicode-notification-div").fadeIn();
                $(".div_vat").fadeIn();
            } else {
                // Slow fadeout so user notices what's being removed
                $("#einvoice-operator-div").fadeOut(speed);
                $("#edicode-div").fadeOut(speed);
                $("#edicode-notification-div").fadeOut(speed);
                $(".div_vat").fadeOut(speed);
            }
        }

        $("input[name=company_name]").change(toggleEdicode);
        toggleEdicode();
    });
});
