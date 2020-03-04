odoo.define('website_sale_hide_company_private_customer.hide_company', function (require){
"use strict";

    $(function() {
        $("label[for='company_name']").toggleClass('d-none');
        $("input[name='company_name']").toggleClass('d-none');
    });
    $('#is_company').click(function() {
            var is_company = $('#is_company').is(':checked');

            if (is_company === true) {
                $('#is_company').attr('checked', 'checked');
                $("label[for='company_name']").removeClass('d-none');
                $("input[name='company_name']").removeClass('d-none');
            } else {
                $('#is_company').removeAttr('checked');
                $("label[for='company_name']").toggleClass('d-none', !is_company);
                $("input[name='company_name']").toggleClass('d-none', !is_company);
            }
    });
});
