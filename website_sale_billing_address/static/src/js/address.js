odoo.define('website_sale_billing_address.address', function (require) {
    "use strict";

    $(function() {
        $("#billing_use_same").change(function() {
            if(this.checked) {
                $(".billing_to_other").hide()
            }else{
                $(".billing_to_other").show()
            }
        });
    });
});
