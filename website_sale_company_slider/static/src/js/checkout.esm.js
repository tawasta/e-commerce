/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteSaleCompanySlider = publicWidget.Widget.extend({
    selector: ".oe_website_sale",
    events: {
        "click #company": "_onToggleCompanyFields",
    },

    start() {
        this._super(...arguments);
        this._showFields();
    },

    _onToggleCompanyFields: function () {
        this._showFields();
    },

    _showFields: function () {
        const $fieldRequired = $("input[name='field_required']");
        const isCompany = $("#company").is(":checked");
        let fieldRequiredVal = null;

        if ($fieldRequired.length > 0) {
            fieldRequiredVal = $fieldRequired.val();
        }

        if ($fieldRequired.length > 0) {
            // Reset required fields set
            $fieldRequired.val(fieldRequiredVal);
        }

        // Company customer
        $("#is_company_label_true")
            .toggleClass("text-primary", isCompany)
            .toggleClass("text-muted", !isCompany);
        // Private customer
        $("#is_company_label_false")
            .toggleClass("text-primary", !isCompany)
            .toggleClass("text-muted", isCompany);

        // Toggle fields as required by customer type
        $("label[for='company_name']").toggleClass(
            "label-optional font-weight-normal",
            !isCompany
        );
        $("label[for='company_email']").toggleClass(
            "label-optional font-weight-normal",
            !isCompany
        );

        // Toggle field visibility by customer type
        $("input[name='company_name']").parent().toggleClass("d-none", !isCompany);
        if (!isCompany) {
            $("input[name='company_name']").val("");
            $("input[name='company_email']").val("");
            $("input[name='vat']").val("");
            $("input[name='edicode']").val("");
            $("#einvoice-operator-select").val("").trigger("change");
        }

        $("input[name='company_email']").parent().toggleClass("d-none", !isCompany);
        $("input[name='vat']").parent().toggleClass("d-none", !isCompany);

        $(".div_vat").toggleClass("d-none", !isCompany);
        $(".show-company").toggleClass("d-none", !isCompany);
        $(".hide-company").toggleClass("d-none", isCompany);
        $("#private_title").toggleClass("d-none", isCompany);
        $("#company_title").toggleClass("d-none", !isCompany);

        if (isCompany && $fieldRequired.val().indexOf(",company_name,vat") < 0) {
            $fieldRequired.val($fieldRequired.val() + ",company_name,vat");
        } else if (!isCompany && $fieldRequired.length > 0) {
            $fieldRequired.val($fieldRequired.val().replace(",company_name,vat", ""));
        }
    },
});

export default publicWidget.registry.WebsiteSaleCompanySlider;
