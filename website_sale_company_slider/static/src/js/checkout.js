odoo.define("website_sale_company_slider.checkout", function (require) {
    "use strict";

    $(function () {
        if ($("#company").length != 0) {
            var field_required = $("input[name='field_required']");
            const REQUIRED_FIELDS_DEFAULT = null;

            if (field_required.length > 0) {
                const REQUIRED_FIELDS_DEFAULT = field_required.val();
            }

            function showFields() {
                var is_company = $("#company").is(":checked");

                var required_fields = $("input[name='field_required']");
                if (required_fields.length > 0) {
                    // Reset required fields set
                    required_fields.val(REQUIRED_FIELDS_DEFAULT);
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
                $("input[name='company_name']")
                    .parent()
                    .toggleClass("d-none", !is_company);
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
                    if (required_fields.val().indexOf(",company_name,vat") < 0) {
                        required_fields.val(
                            required_fields.val() + ",company_name,company_email,vat"
                        );
                    }
                } else if (required_fields.length > 0) {
                    required_fields.val(
                        required_fields
                            .val()
                            .replace(",company_name,company_email,vat", "")
                    );
                }
            }

            showFields();
            $("#company").click(function () {
                showFields();
            });
        }
    });
});
