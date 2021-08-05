 window.addEventListener('load',  function() {
    var star = ""
    var directories = $(location).attr('href').split("/");
    var category =  directories[directories.length - 2];
   $("#star1").click(function(){
       star = $("#star1").val()
});

$("#star2").click(function(){
    star = $("#star2").val()
});
$("#star3").click(function(){
    star = $("#star3").val()
});
$("#star4").click(function(){
    star = $("#star4").val()
});
$("#star5").click(function(){
    star = $("#star5").val()
});







});