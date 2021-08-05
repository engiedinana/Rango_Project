window.addEventListener('load',  function() {
   var xhr = new XMLHttpRequest();
   var k;
   var ratup = `<span class="fa fa-star checked"></span>`
   var ratdown = `<span class="fa fa-star"></span>`
   xhr.onreadystatechange = function() {
      if (xhr.readyState == XMLHttpRequest.DONE) {
         const k = JSON.parse(xhr.responseText);
         var html=""
         for(var i = 0; i < k.categories.length; i++){
            console.log(k.categories[i].title)
               html = html + `<div class="article">
                           <div id = "image_container"><img class="image" src="/media/`+k.categories[i].image+`"> </div>
                           <div>
                              <h2> <a class = "Cat-name" href= /rango/category/`+ k.categories[i].slug +`>` + k.categories[i].title + `</a></h2>
                              <p>`
                              for(var z=0;z<5;z++){
                                 if(z<=k.categories[i].rating-1){
                                    html = html + ratup;
                                 }else{
                                 html = html + ratdown;
                                 }
                              }
                              
               html = html + ` </p>`
            for(var j = 0; j < k.categories[i].pages.length; j++){
               console.log(k.categories[i].pages[j])
               html = html + `
                                 <a href=` + k.categories[i].pages[j].url + ` data-toggle="tooltip" title = "`+ k.categories[i].pages[j].description + `" > ` +k.categories[i].pages[j].title+`</a> </br>`
            }
            html = html + `
                        </div> 
                  </div>`
         }
         document.getElementById('archive').innerHTML = html
      }
  }
   xhr.open("GET", "/rango/get_cat", true);
   xhr.send(null);
   
$('.AlphabetNav a').click(function(evt) {
   evt.preventDefault();
   var $navItem = $(this),
   $articles = $('.article');
   $articles.show();
   
   if ($navItem.hasClass('active')) {
     $navItem.removeClass('active');
   } else {
      $('.AlphabetNav a').removeClass('active');
      $navItem.addClass('active');

      if($navItem.text().toLowerCase() != "all"){
         

      $.each($articles, function(key, article) {
            var $article = $(article),
               $CatName = $article.find('.Cat-name'),
               $nameArr = $CatName.text().split(' ');
            if ($nameArr[0].split('')[0].toLowerCase() !== $navItem.text().toLowerCase()) {
            $article.hide();
      }
    });
   }
       }
 }); 
});
