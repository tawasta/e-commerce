odoo.define("website_sale_edicode.checkout", function (require) {
    "use strict";
    var core = require("web.core");
    var _t = core._t;

    $(function () {
        // eslint-disable-next-line no-unused-vars
        function toggleEdicode() {
            var company_name = $("input[name=company_name]");
            if (company_name.length === 0) {
                return;
            }

            var company = company_name.val().length !== 0;
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

        if ($("#einvoice-operator-select").length !== 0) {
            $("#einvoice-operator-select").select2({
                allowClear: true,
            });

            // Uncommenting these will enable auto-hide for edicode-fields
            // $("input[name=company_name]").change(toggleEdicode);
            // toggleEdicode();

            $("form[class$='checkout_autoformat']").on("click", ".a-submit", function (
                e
            ) {
                var edicode = $("input[name$='edicode']");
                var einvoice_operator = $("select[name$='einvoice_operator_id']");
                var company_name = $("input[name=company_name]");
                if (
                    (edicode.val() && einvoice_operator.val()) ||
                    (!edicode.val() && !einvoice_operator.val()) ||
                    !company_name.val()
                ) {
                    console.log("Edicode validation successful");
                } else {
                    e.preventDefault();
                    e.stopPropagation();
                    if ($("h5[class$='text-danger']").length) {
                        $("h5[class$='text-danger']").empty();
                        $("h5[class$='text-danger']").append(
                            _t(
                                "<p>Fill in both eInvoice address and eInvoice Operator.</p>"
                            )
                        );
                    } else {
                        $("form[class$='checkout_autoformat']").before(
                            _t(
                                "<h5 class='text-danger'><p>Fill in both eInvoice address and eInvoice Operator.</p></h5>"
                            )
                        );
                    }
                    $("html, body").animate({scrollTop: 0}, "slow");
                }
            });
        }
    });
});
