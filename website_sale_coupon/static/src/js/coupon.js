odoo.define('proposal', function (require) {
    var _t = require('web.core')._t;

    var ajax = require('web.ajax');

    $(function() {
        // Prevent sending with enter press
        $('#btn-coupon-submit, #coupon-code').keypress(function (event) {
            if (event.keyCode === 10 || event.keyCode === 13) {
                event.preventDefault();
                return false;
            }
        });

        // When coupon is submitted, try to use it and display error/success
        $('#btn-coupon-submit').click(function(event){
            event.preventDefault();

            var action = "/shop/coupon/use";
            var code = $('#coupon-code').val();

            ajax.jsonRpc(action, 'call', {'code': code}).then(function(data){
                if(data.error){
                    $('#coupon-code-error').text(data.error);
                    // Hackish way to use show because Bootstrap has !important for .hidden
                    $('#coupon-code-error').removeClass('hidden').hide().fadeIn();
                } else {
                    // Reload to update prices
                    location.reload();
                }
            });
        });

        // When deleting a product or a coupon product, remove the coupon log entry
        $('.js_delete_product').click(function(){
            var action = "/shop/coupon/remove";
            var row = $(this).closest('tr');

            var coupon_id = row.find('.js_coupon').attr('data-coupon-id');

            var values = {'coupon_id': coupon_id};

            ajax.jsonRpc(action, 'call', values).then(function(data){
                // This could show an info message, but it shouldn't be necessary
            });
        });

    });
});