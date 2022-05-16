var fade_time = 300;

$(function(){
    $('.product-quantity input').change( function() {
        var item_name = $(this).attr("item-name");
        var item_val = this.value;
        var tag = this;
        var cart = $(this).parent().parent().parent().children(".cart_info").children(".checkout").attr("value");

        $.ajax(
        {
            type:"GET",
            url: "/quantity_change",
            data:{
                    item_name: item_name,
                    item_val: item_val,
                    cart: cart,
            },
            success: function( data ) 
            {
                var obj = JSON.parse(data);
                var t = $(tag).parent().parent();
                
                // update cart info
                $(tag).parent().parent().parent().children(".cart_info").children(".checkout").attr("value", obj['cart_str']);
        
                t.children(".product-line-price").each(function () {
                    $(this).fadeOut(fade_time, function() {
                        $(this).text(obj['item_total']);
                        $(this).fadeIn(fade_time);
                    });
                });
                t.parent().children(".totals").children(".totals-item").children("#cart-subtotal").each(function () {
                    $(this).fadeOut(fade_time, function() {
                        $(this).text(obj['sub_total']);
                        $(this).fadeIn(fade_time);
                    });
                });
                t.parent().children(".totals").children(".totals-item").children("#cart-tax").each(function () {
                    $(this).fadeOut(fade_time, function() {
                        $(this).text(obj['tax']);
                        $(this).fadeIn(fade_time);
                    });
                });
                t.parent().children(".totals").children(".totals-item").children("#cart-shipping").each(function () {
                    $(this).text(obj['shipping']);
                });
                t.parent().children(".totals").children(".totals-item").children("#cart-total").each(function () {
                    $(this).fadeOut(fade_time, function() {
                        $(this).text(obj['grand_total']);
                        $(this).fadeIn(fade_time);
                    });
                });
            }
        })
    });
    
    $('.product-removal button').click( function() {
        var productRow = $(this).parent().parent();
        var item_name = $(this).attr("item-name");
        var tag = this;
        var cart = $(this).parent().parent().parent().children(".cart_info").children(".checkout").attr("value");

        productRow.slideUp(fade_time, function() {
            productRow.remove();
        });

        $.ajax(
            {
                type:"GET",
                url: "/remove_item",
                data:{
                        item_name: item_name,
                        cart: cart,
                },
                success: function( data ) 
                {
                    var obj = JSON.parse(data);
                    var t = $(tag).parent().parent().parent().children(".totals").children(".totals-item");
                    
                    // update cart info
                    $(tag).parent().parent().parent().children(".cart_info").children(".checkout").attr("value", obj['cart_str']);

                    t.children("#cart-subtotal").each(function () {
                        $(this).fadeOut(fade_time, function() {
                            $(this).text(obj['sub_total']);
                            $(this).fadeIn(fade_time);
                        });
                    });
                    t.children("#cart-tax").each(function () {
                        $(this).fadeOut(fade_time, function() {
                            $(this).text(obj['tax']);
                            $(this).fadeIn(fade_time);
                        });
                    });
                    t.children("#cart-shipping").each(function () {
                        $(this).text(obj['shipping']);
                    });
                    t.children("#cart-total").each(function () {
                        $(this).fadeOut(fade_time, function() {
                            $(this).text(obj['grand_total']);
                            $(this).fadeIn(fade_time);
                        });
                    });
                }
            })
    });
});