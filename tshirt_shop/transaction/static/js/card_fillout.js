$(function () {
    $('.cc-number').formatCardNumber();
    $('.cc-expires').formatCardExpiry();
    $('.cc-cvc').formatCardCVC();
    $('#phone').inputmask({"mask": "999-999-9999"})

});