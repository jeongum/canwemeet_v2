$(document).ready(function(){
    $("#create-room").click(function(){
        $("#create-room-popup").fadeIn();
    });
    $(".cancel").click(function(){
        $("#create-room-popup").fadeOut();
    });
});