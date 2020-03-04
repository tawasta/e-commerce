odoo.define('website_sale_hide_company_private_customer.hide_company', function (require){
"use strict";

    const REQUIRED_FIELDS_DEFAULT = $("input[name='field_required']").val();
    const FI_COUNTRY_ID = $('#fi_country_id').val();
    $(function() {
        $("label[for='company_name']").addClass('d-none');
        $("input[name='company_name']").addClass('d-none');
    });
    $('#is_company').click(function() {
            var is_company = $('#is_company').is(':checked');
            var required_fields = $("input[name='field_required']");
            // Reset required fields set
            required_fields.val(REQUIRED_FIELDS_DEFAULT);
            
            // Company customer
            $("label[id='is_company_label_true']").toggleClass('text-primary', is_company);
            $("label[id='is_company_label_true']").toggleClass('text-muted', !is_company);

            // Private customer
            $("label[id='is_company_label_false']").toggleClass('text-primary', !is_company);
            $("label[id='is_company_label_false']").toggleClass('text-muted', is_company);

            // Toggle fields by customer type
            $("label[for='company_name']").toggleClass('label-optional', is_company);
            $("label[for='vat']").toggleClass('label-optional', is_company);

            $(".div_vat").toggleClass('d-none', !is_company);
            $(".show-company").toggleClass('d-none', !is_company);
            $(".hide-company").toggleClass('d-none', is_company);

            if (is_company === true) {
                $('#is_company').attr('checked', 'checked');
                $("label[for='company_name']").removeClass('d-none');
                $("input[name='company_name']").removeClass('d-none');
                if (required_fields.val().indexOf(',company_name,vat') < 0) {
                    required_fields.val(required_fields.val() + ',company_name,vat');
                }
            } else {
                $('#is_company').removeAttr('checked');
                $("label[for='company_name']").addClass('d-none');
                $("input[name='company_name']").addClass('d-none');
                required_fields.val(required_fields.val().replace(',company_name,vat', ''));
            }
    });
});