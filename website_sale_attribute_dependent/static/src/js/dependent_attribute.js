odoo.define('website_sale_dependent_attribute.dependent_attribute', function (require) {
    "use strict";
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');

    $(function() {
        $('.js_variant_change').change(function() {
            var value_id = $(this).data('value_id');
            var attribute_name = $(this).data('attribute_name');

            // Get all values that are dependant to the changed value
            rpc.query({
                model: 'product.attribute.value',
                method: 'search',
                args: [[['dependency_id', '=', value_id]]],
            }).then(function (attributes) {
                $.each(attributes, function(index, value){
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