/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteSaleInvoiceTransmitMethod = publicWidget.Widget.extend({
    selector: ".oe_website_sale",
    events: {
        "change #customer-invoice-transmit-method-billing": "_onToggleVisibility",  // Päivitetty ID
    },

    start() {
        this._super(...arguments);
        this._onToggleVisibility(); // Muutettu kutsumaan oikein määriteltyä funktiota
    },

    _onToggleVisibility() {
        const transmitType = $("#customer-invoice-transmit-method-billing").find(":selected").data("code");
        const fieldRequiredInput = $("input[name='field_required']");
        let fieldRequiredVal = fieldRequiredInput.val() || "";

        // Resetoidaan kenttien oletusarvot
        this._resetFields();

        // Manage visibility and required fields based on transmitType
        const actions = {
            "mail": () => $("label[for='company_email']").removeClass("label-optional"),
            "post": () => {
                this._hideCompanyEmail();
                fieldRequiredVal = this._removeFieldFromRequiredList(fieldRequiredVal, "company_email");
            },
            "einvoice": () => {
                $("label[for='vat']").removeClass("label-optional");
                this._hideCompanyEmail();
                fieldRequiredVal = this._removeFieldFromRequiredList(fieldRequiredVal, "company_email");
                this._showEinvoiceFields();
            }
        };

        // Execute corresponding action if exists
        if (actions[transmitType]) actions[transmitType]();

        // Update fieldRequired input
        fieldRequiredInput.val(fieldRequiredVal);
    },

    _resetFields() {
        $("label[for='company_email'], label[for='vat'], label[for='einvoice_operator_id'], label[for='edicode']").addClass("label-optional");
        $("#company_email").show();
        $("#einvoice-operator-div, #edicode-div, #edicode-notification-div").hide();
    },

    _hideCompanyEmail() {
        $("#company_email").hide();
        $("#company-email-input").val("");
    },

    _showEinvoiceFields() {
        $("#einvoice-operator-div, #edicode-div, #edicode-notification-div").fadeIn("slow");
    },

    _removeFieldFromRequiredList(fieldRequiredVal, fieldName) {
        return fieldRequiredVal.replace(`${fieldName},`, "");
    },
});

export default publicWidget.registry.WebsiteSaleInvoiceTransmitMethod;
