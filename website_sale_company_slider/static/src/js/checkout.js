odoo.define('website_sale_company_slider.checkout', function (require) {
    "use strict";

    var _t = require('web.core')._t;

    $(function() {

        const REQUIRED_FIELDS_DEFAULT = $("input[name='field_required']").val();
        const FI_COUNTRY_ID = $('#fi_country_id').val();
        $("input[name='company_name']").removeClass('d-none');
        
        function showFields() {
            var is_company = $('#is_company').is(':checked');
            console.log(is_company);
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
            $("label[for='company_name']").toggleClass('d-none', !is_company);
            $("input[name='company_name']").toggleClass('d-none', !is_company);
            $(".show-company").toggleClass('d-none', !is_company);
            $(".hide-company").toggleClass('d-none', is_company);

            if (is_company === true) {
                console.log("COMPANY ON TRUE");
                $('#is_company').attr('checked', 'checked');
                $("label[for='company_name']").removeClass('d-none');
                console.log($("label[for='company_name']").removeClass('d-none'));
                $("input[name='company_name']").removeClass('d-none');
                console.log($("input[name='company_name']").removeClass('d-none'));
                if (required_fields.val().indexOf(',company_name,vat') < 0) {
                    required_fields.val(required_fields.val() + ',company_name,vat');
                }
            } else {
                $('#is_company').removeAttr('checked');
                required_fields.val(required_fields.val().replace(',company_name,vat', ''));
            }
        }
        showFields();
        $('#is_company').click(function() {
            showFields();
        });

        $('.oe_website_sale .a-submit, #comment .a-submit').off('click').on('click', function (event) {
            if (!event.isDefaultPrevented() && !$(this).is(".disabled")) {
                var form = $(this).closest('form');
                var is_company = $('#is_company').is(':checked');
                if (is_company === false) {
                    // Empty company related fields
                    $('.show-company').val('');
                    $('input[name="vat"]').val('');
                }
                // If country is Finland and VAT is inserted, make business id
                var vat = $(form).find("input[name='vat']").val();
                var country_id = $('#country_id').val();

                if (vat && country_id === FI_COUNTRY_ID) {
                    var parsed = vat.replace(/[^0-9]/g, '');
                    var business_id = parsed.substr(0, 7) + '-' + parsed.substr(7, 1);
                    $(form).append('<input type="hidden" name="business_id" value="' + business_id + '"/>');
                }
                $(this).closest('form').submit();
            }
            if ($(this).hasClass('a-submit-disable')){
                $(this).addClass("disabled");
            }
            if ($(this).hasClass('a-submit-loading')){
                var loading = '<span class="fa fa-cog fa-spin"/>';
                var fa_span = $(this).find('span[class*="fa"]');
                if (fa_span.length){
                    fa_span.replaceWith(loading);
                }
                else{
                    $(this).append(loading);
                }
            }
        });
    });
});
