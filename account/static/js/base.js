
function validateNumber(evt){
    var theEvent = evt || window.event;
    var key = theEvent.keyCode || theEvent.which;

    if ((key < 48 || key > 57) && !(key == 8 || key == 9 || key == 13 || key == 37 || key == 39 || key == 46)){
        theEvent.returnValue = false;

        if (theEvent.preventDefault) theEvent.preventDefault();
    }
}

$(function() {
    $('#btnSignUp').click(function() {
 
        $.ajax({
            url: '.',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

$(function() {
    $("form[name='registration']").validate({
        rules:{
            username: {
                required: true,
                minlength: 4
            },
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                minlength: 4
            }
        },
        messages:{
            username: {
                required: "Please enter your username",
                minlength: "Your username must be at least 4 characters long"
            },
            password: {
                required: "Please provide a password",
                minlength: "Your password must be at least 4 characters long"
            },
            email: "Please enter a valid email address"
        },
        submitHandler: function(form){
            form.submit();
        }
    });
});

/*
$(document).ready(function()){
    $("#inputPhoneNumber").keydown(function(e){
        // Allow backspace, delete, tab, escape, enter 
        if($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
            // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) ||
            // Allow: Ctrl+C
            (e.keyCode == 67 && e.ctrlKey === true) ||
            // Allow: Ctrl+X
            (e.keyCode == 88 && e.ctrlKey === true) ||
            // Allow: home, end, left, right
            (e.keyCode == 35 && e.ctrlKey <= 39)){

            // let it happen, don't do anything
            return;
        }

        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && 
            (e.keyCode < 96 || e.keyCode > 105)){
            e.preventDefault();
        }
    });
});

$(function() {
    $('#btnSignUp').click(function() {
 
        $.ajax({
            url: '.',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

*/
