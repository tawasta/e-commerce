odoo.define('website_sale_product_tracking.track_product', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.TrackProductButton = publicWidget.Widget.extend({
        selector: '.oe_website_sale',
        xmlDependencies: [],

        start: function () {
            this._super.apply(this, arguments);
            var self = this;
            this.$('.tracking-product').click(function (ev) {
                ev.preventDefault();
                
                var product_id = $(this).attr('data-product-id'); // Hae tuote-ID painikkeesta
                self.$('#hidden-product-id').val(product_id); // Aseta tuote-ID piilotettuun syöttökenttään
                
                self.$('#modaltracking').modal('show'); // Näytä modaalilomake
            });

            this.$('#track-product-form').submit(function (ev) {
                ev.preventDefault();
                
                var email = self.$('#email').val();
                var product_id = self.$('#hidden-product-id').val(); // Hae tuote-ID piilotetusta syöttökentästä
                ajax.jsonRpc('/my/add_product_tracking', 'call', {
                    'email': email,
                    'product_id': product_id,
                }).then(function (result) {
                    $.toast({
                        title: ("Success!"),
                        subtitle: ("Product added to tracking!"),
                        content: result["msg"],
                        type: "success",
                        delay: 5000,
                        dismissible: true
                    });
                    self.$('#modaltracking').modal('hide');
                }).catch(function () {
                    //$.toast.error('Jotain meni pieleen.');
                });
            });
        },
    });
});
