odoo.define('website_sale_show_product_code.website_sale_show_product_code', function(require) {

    var ajax = require('web.ajax');

    $(document).ready(function () {

        $("input.js_variant_change, select.js_variant_change").change(function(ev) {
            /* When attribute selections change, find the variant that matches
            the selected attributes by using the same logic as in website_sale */
            var $ul = $(ev.target).closest('.js_add_cart_variants');
            var $parent = $ul.closest('.js_product');
            var variant_ids = $ul.data("attribute_value_ids");
            var values = [];
            var unchanged_values = $parent.find('div.oe_unchanged_value_ids').data('unchanged_value_ids') || [];
            var default_code_selector = ".product-variant-default-code";

            $parent.find('input.js_variant_change:checked, select.js_variant_change').each(function () {
                values.push(+$(this).val());
            });

            values =  values.concat(unchanged_values);
            var product_id = false;

            for (var k in variant_ids) {
                if (_.isEmpty(_.difference(variant_ids[k][1], values))) {
                    product_id = variant_ids[k][0];
                    break;
                }
            }

            if(product_id) {
                // If a variant exists for the attribute combination,
                // query its internal reference from the backend
                ajax.jsonRpc('/shop/get_variant_code/', "call", {
                    "product_id": product_id,
                }).then(function (data) {
                    $(default_code_selector).text(data['code']);
                });
            }
            else {
                // If an impossible attribute combination was selected,
                // clear the shown internal reference
                $(default_code_selector).text('-');
            }

            // Trigger after being bound so that the code shows up also after
            // the product page initally loads.
        }).change();
    });
});
