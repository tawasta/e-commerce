$(document).ready(function () {
    'use strict';

    $('#shipping-address-search').bind('keyup', function(){
        var search_text = $(this).val().toLowerCase();

        // All addresses
        var addrs = $('.all_shipping .col-lg-6.one_kanban');

        // Show all
        addrs.removeClass('d-none');

        if (search_text) {
            var not_matching = addrs.filter(function() {
                // Find all elements not matching to search
                var address = $(this).find("span[itemprop='name']").text();

                return address.toLowerCase().indexOf(search_text) < 0;
            });

            // Hide not matching items
            not_matching.addClass('d-none');
        }
    });
});
