window.addEventListener('load',  function() {
    var star = ""
    var directories = $(location).attr('href').split("/");
    var category =  directories[directories.length - 2];
    var xhr = new XMLHttpRequest();
   $("#star1").click(function(){
       star = $("#star1").val()
       xhr.onreadystatechange = function() {}
       xhr.open("GET", `/rango/rate_category/`+category +`/`+star, true);
       xhr.send(null);
});

$("#star2").click(function(){
    star = $("#star2").val()
    xhr.onreadystatechange = function() {}
       xhr.open("GET", `/rango/rate_category/`+category +`/`+star, true);
       xhr.send(null);
});
$("#star3").click(function(){
    star = $("#star3").val()
    xhr.onreadystatechange = function() {}
       xhr.open("GET", `/rango/rate_category/`+category +`/`+star, true);
       xhr.send(null);
});
$("#star4").click(function(){
    star = $("#star4").val()
    xhr.onreadystatechange = function() {}
       xhr.open("GET", `/rango/rate_category/`+category +`/`+star, true);
       xhr.send(null);
});
$("#star5").click(function(){
    star = $("#star5").val()
    xhr.onreadystatechange = function() {}
       xhr.open("GET", `/rango/rate_category/`+category +`/`+star, true);
       xhr.send(null);
});



});