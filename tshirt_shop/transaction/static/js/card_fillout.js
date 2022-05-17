$(function () {
    $('.cc-number').formatCardNumber();
    $('.cc-expires').formatCardExpiry();
    $('.cc-cvc').formatCardCVC();
    $('#phone').inputmask({"mask": "999-999-9999"})
    

    fetch("/config/")
    .then((result) => { return result.json(); })
    .then((data) => {
        const stripe = Stripe(data.publicKey);
        document.querySelector("#submitBtn").addEventListener("click", () => {
            $.ajax(
                {
                    type:"GET",
                    url: "/stripe_session",
                    data:{
                        firstname: document.getElementById("firstname").value,
                        lastname: document.getElementById("lastname").value,
                        shipping_address: document.getElementById("shipping_address").value,
                        shipping_city: document.getElementById("shipping_city").value,
                        shipping_state: document.getElementById("shipping_state").value,
                        shipping_zip: document.getElementById("shipping_zip").value,
                        phone: document.getElementById("phone").value,
                        email: document.getElementById("email").value,
                        cart_info: document.getElementById("cart_info").value,
                        
                    },
                    success: function( data ) 
                    {
                        // var obj = JSON.parse(data);
                        return stripe.redirectToCheckout({sessionId: data.sessionId})
                    }
                })
        });
    });
});