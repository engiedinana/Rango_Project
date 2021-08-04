window.addEventListener('load',  function() {
   //document.getElementById("greeting").innerHTML = "BAKRAHKO KOLOKO"
   var xhr = new XMLHttpRequest();
   var k;
   xhr.onreadystatechange = function() {
      if (xhr.readyState == XMLHttpRequest.DONE) {
         var block_to_insert ;
         var container_block ;
         const k = JSON.parse(xhr.responseText);
         var html=""
         for(var i = 0; i < k.categories.length; i++){
            console.log(k.categories[i].title)
               html = html + `<div class="column">
                        <div class="card">
                           <img class = "img" src="/static/images/`+k.categories[i].image+`">
                           <div class="container">
                              <h2>` + k.categories[i].title + `</h2>
                              <p class="title"> Rating: `+k.categories[i].rating+`</p>
                              <ul>`
            for(var j = 0; j < k.categories[i].pages.length; j++){
               console.log(k.categories[i].pages[j])
               html = html + `<li>
                                 <a href=` + k.categories[i].pages[j].url +`>`+k.categories[i].pages[j].title+`</a>
                              </li>`
            }
            html = html + `</ul> 
                        </div> 
                     </div>
                  </div>`
         }
         document.getElementById('row').innerHTML = html
      }
  }
   xhr.open("GET", "get_cat", true);
   xhr.send(null);
});