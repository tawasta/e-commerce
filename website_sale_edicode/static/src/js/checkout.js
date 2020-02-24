odoo.define('website_sale_edicode.checkout', function (require) {
    "use strict";

    $(function() {
        $('#einvoice-operator-select').select2();

        function toggleTransmitMethod() {
            // If the selector exists, toggle visibility
            console.log('ding');
            console.log($("#customer-invoice-transmit-method"));
            if($('#customer-invoice-transmit-method').length){
                var transmit_method = $('#customer-invoice-transmit-method');
                var code = transmit_method.find(':selected').data('code');

                var einvoice = code == 'einvoice';
                // Show einvoice address and operator if transmit method is einvoice
                $('#einvoice-operator-div').toggleClass('d-none', !einvoice);
                $('#edicode-div').toggleClass('d-none', !einvoice);
            }
        }

        $('#customer-invoice-transmit-method').change(toggleTransmitMethod);
        toggleTransmitMethod();
    });
});
