odoo.define("website_sale_company_slider.checkout", function () {
    "use strict";

    $(function () {
        function showFields() {
            var field_required = $("input[name='field_required']");

            var field_required_val = null;
            var is_company = $("#company").is(":checked");

            if (field_required.length > 0) {
                field_required_val = field_required.val();
            }

            if (field_required.length > 0) {
                // Reset required fields set
                field_required.val(field_required_val);
            }

            // Company customer
            $("label[id='is_company_label_true']").toggleClass(
                "text-primary",
                is_company
            );
            $("label[id='is_company_label_true']").toggleClass(
                "text-muted",
                !is_company
            );

            // Private customer
            $("label[id='is_company_label_false']").toggleClass(
                "text-primary",
                !is_company
            );
            $("label[id='is_company_label_false']").toggleClass(
                "text-muted",
                is_company
            );

            // Toggle fields as required by customer type
            $("label[for='company_name']").toggleClass(
                "label-optional font-weight-normal",
                !is_company
            );
            $("label[for='company_email']").toggleClass(
                "label-optional font-weight-normal",
                !is_company
            );

            // Toggle field visibility by customer type
            $("input[name='company_name']").parent().toggleClass("d-none", !is_company);
            if (!is_company) {
                $("input[name='company_name']").val("");
                $("input[name='company_email']").val("");
                $("input[name='vat']").val("");
                $("input[name='edicode']").val("");
                $("#einvoice-operator-select").select2("val", "");
            }

            $("input[name='company_email']")
                .parent()
                .toggleClass("d-none", !is_company);
            $("input[name='vat']").parent().toggleClass("d-none", !is_company);

            $(".div_vat").toggleClass("d-none", !is_company);
            $(".show-company").toggleClass("d-none", !is_company);
            $(".hide-company").toggleClass("d-none", is_company);
            $("#private_title").toggleClass("d-none", is_company);
            $("#company_title").toggleClass("d-none", !is_company);

            if (is_company === true) {
                if (field_required.val().indexOf(",company_name,vat") < 0) {
                    field_required.val(
                        field_required.val() + ",company_name,company_email,vat"
                    );
                }
            } else if (field_required.length > 0) {
                field_required.val(
                    field_required.val().replace(",company_name,company_email,vat", "")
                );
            }
        }

        if ($("#company").length !== 0) {
            showFields();
            $("#company").click(function () {
                showFields();
            });
        }
    });
});
