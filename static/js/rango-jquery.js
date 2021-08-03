$(".navbar-toggle").on("click", function() {

    $(".overlay").fadeIn("slow")
  
  })
  $(".overlay").on("click", function() {
  
    $(this).fadeOut();
    $(".navbar-collapse").removeClass("in").addClass("collapse")
})