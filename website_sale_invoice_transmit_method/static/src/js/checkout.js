odoo.define("website_sale_invoice_transmit_method.checkout", function () {
    "use strict";

    $(function () {
        function toggleVisibility() {
            var field_required = $("input[name='field_required']");
            var field_required_val = field_required.val();
            var field_required_val = "";

            if (field_required.length > 0) {
                field_required_val = field_required.val();
            }

            var transmit_type = $("#customer-invoice-transmit-method")
                .find(":selected")
                .data("code");
            var speed = "slow";

            // Initial values
            $("label[for='company_email']").addClass("label-optional");
            $("#company_email").show();

            $("label[for='vat']").addClass("label-optional");

            $("label[for='einvoice_operator_id']").addClass("label-optional");
            $("label[for='edicode']").addClass("label-optional");

            $("#einvoice-operator-div").hide();
            $("#edicode-div").hide();
            $("#edicode-notification-div").hide();

            if (transmit_type === "mail") {
                // Refers to website_sale_company_email
                $("label[for='company_email']").removeClass("label-optional");
            } else if (transmit_type == "post") {
                // Refers to website_sale_company_email
                $("#company_email").hide();
                $("#company-email-input").val("");
                // Set company email as not required
                field_required.val(field_required_val.replace("company_email,", ""));
            } else if (transmit_type === "einvoice") {
                // Refers to website_sale_business_code
                $("label[for='vat']").removeClass("label-optional");

                // Refers to website_sale_company_email
                $("#company_email").hide();
                $("#company-email-input").val("");

                // Set company email as not required
                field_required.val(field_required_val.replace("company_email,", ""));

                // Refers to website_sale_edicode
                $("label[for='einvoice_operator_id']").removeClass("label-optional");
                $("label[for='edicode']").removeClass("label-optional");

                $("#einvoice-operator-div").fadeIn(speed);
                $("#edicode-div").fadeIn(speed);
                $("#edicode-notification-div").fadeIn(speed);
            }
        }

        $("#customer-invoice-transmit-method").change(toggleVisibility);
        toggleVisibility();
    });
});
