odoo.define('website_sale_edicode.checkout', function (require) {
    "use strict";

    $(function() {
        $('#einvoice-operator-select').select2();

        function toggleEdicode() {
            var company = $("input[name=company_name]").val().length != 0
            if(company){
                $('#einvoice-operator-div').fadeIn();
                $('#edicode-div').fadeIn();
                $('.div_vat').fadeIn();
            } else{
                // Slow fadeout so user notices what's being removed
                $('#einvoice-operator-div').fadeOut("slow");
                $('#edicode-div').fadeOut("slow");
                $('.div_vat').fadeOut("slow");
            }
        }

        $("input[name=company_name]").change(toggleEdicode);
        toggleEdicode();
    });
});
