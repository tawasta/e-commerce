odoo.define('website_sale_dependent_attribute.dependent_attribute', function (require) {
    "use strict";
    var ajax = require('web.ajax');

    $(function() {
        $('.js_variant_change').change(function() {
            // The selected value
            var value_id = parseInt($(this).data('value_id'));

            // Controller to call
            var action = "/attribute/value/get/dependencies";

            // Prepare values to send for controller
            var values = {
                'id': value_id,
            };

            // Get all values that are dependant to the changed value
            ajax.jsonRpc(action, 'call', values).then(function(attributes){
                $.each(attributes, function(index, value){
                    // Loop through all dependent attributes

                    // Try to find both inputs and options with this id
                    var input = $("input.js_variant_change[data-value_id='"+value+"']");
                    var option = $(".js_variant_change option[data-value_id='"+value+"']");

                    if(input.length > 0){
                        // Change inputs (radio and color)
                        input.prop("checked", true).trigger("change");
                    } else if(option.length > 0){
                        // Change options (select)
                        option.parent().val(option.val());
                    }
                });
            });
        });
    });
});