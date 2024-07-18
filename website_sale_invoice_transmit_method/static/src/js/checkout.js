/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteSaleInvoiceTransmitMethod = publicWidget.Widget.extend({
    selector: '.oe_website_sale',
    events: {
        'change #customer-invoice-transmit-method': '_onToggleVisibility',
    },

    start() {
        this._super(...arguments);
        this._toggleVisibility();
    },

    _onToggleVisibility: function () {
        this._toggleVisibility();
    },

    _toggleVisibility: function () {
        const $fieldRequired = $("input[name='field_required']");
        let fieldRequiredVal = $fieldRequired.val() || "";

        const transmitType = $("#customer-invoice-transmit-method").find(":selected").data("code");
        const speed = "slow";

        // Initial values
        $("label[for='company_email']").addClass("label-optional");
        $("#company_email").show();

        $("label[for='vat']").addClass("label-optional");
        $("label[for='einvoice_operator_id']").addClass("label-optional");
        $("label[for='edicode']").addClass("label-optional");

        $("#einvoice-operator-div").hide();
        $("#edicode-div").hide();
        $("#edicode-notification-div").hide();

        if (transmitType === "mail") {
            // Refers to website_sale_company_email
            $("label[for='company_email']").removeClass("label-optional");
        } else if (transmitType === "post") {
            // Refers to website_sale_company_email
            $("#company_email").hide();
            $("#company-email-input").val("");
            // Set company email as not required
            fieldRequiredVal = fieldRequiredVal.replace("company_email,", "");
            $fieldRequired.val(fieldRequiredVal);
        } else if (transmitType === "einvoice") {
            // Refers to website_sale_business_code
            $("label[for='vat']").removeClass("label-optional");

            // Refers to website_sale_company_email
            $("#company_email").hide();
            $("#company-email-input").val("");

            // Set company email as not required
            fieldRequiredVal = fieldRequiredVal.replace("company_email,", "");
            $fieldRequired.val(fieldRequiredVal);

            // Refers to website_sale_edicode
            $("label[for='einvoice_operator_id']").removeClass("label-optional");
            $("label[for='edicode']").removeClass("label-optional");

            $("#einvoice-operator-div").fadeIn(speed);
            $("#edicode-div").fadeIn(speed);
            $("#edicode-notification-div").fadeIn(speed);
        }
    },
});

export default publicWidget.registry.WebsiteSaleInvoiceTransmitMethod;


// odoo.define("website_sale_invoice_transmit_method.checkout", function () {
//     "use strict";

//     $(function () {
//         function toggleVisibility() {
//             var field_required = $("input[name='field_required']");
//             var field_required_val = field_required.val();
//             var field_required_val = "";

//             if (field_required.length > 0) {
//                 field_required_val = field_required.val();
//             }

//             var transmit_type = $("#customer-invoice-transmit-method")
//                 .find(":selected")
//                 .data("code");
//             var speed = "slow";

//             // Initial values
//             $("label[for='company_email']").addClass("label-optional");
//             $("#company_email").show();

//             $("label[for='vat']").addClass("label-optional");

//             $("label[for='einvoice_operator_id']").addClass("label-optional");
//             $("label[for='edicode']").addClass("label-optional");

//             $("#einvoice-operator-div").hide();
//             $("#edicode-div").hide();
//             $("#edicode-notification-div").hide();

//             if (transmit_type === "mail") {
//                 // Refers to website_sale_company_email
//                 $("label[for='company_email']").removeClass("label-optional");
//             } else if (transmit_type == "post") {
//                 // Refers to website_sale_company_email
//                 $("#company_email").hide();
//                 $("#company-email-input").val("");
//                 // Set company email as not required
//                 field_required.val(field_required_val.replace("company_email,", ""));
//             } else if (transmit_type === "einvoice") {
//                 // Refers to website_sale_business_code
//                 $("label[for='vat']").removeClass("label-optional");

//                 // Refers to website_sale_company_email
//                 $("#company_email").hide();
//                 $("#company-email-input").val("");

//                 // Set company email as not required
//                 field_required.val(field_required_val.replace("company_email,", ""));

//                 // Refers to website_sale_edicode
//                 $("label[for='einvoice_operator_id']").removeClass("label-optional");
//                 $("label[for='edicode']").removeClass("label-optional");

//                 $("#einvoice-operator-div").fadeIn(speed);
//                 $("#edicode-div").fadeIn(speed);
//                 $("#edicode-notification-div").fadeIn(speed);
//             }
//         }

//         $("#customer-invoice-transmit-method").change(toggleVisibility);
//         toggleVisibility();
//     });
// });
