window.addEventListener('load',  function() {
   var xhr = new XMLHttpRequest();
   var k;
   xhr.onreadystatechange = function() {
      if (xhr.readyState == XMLHttpRequest.DONE) {
         const k = JSON.parse(xhr.responseText);
         var html=""
         for(var i = 0; i < k.categories.length; i++){
            console.log(k.categories[i].title)
               html = html + `<div class="article">
                           <img class="image" src="/static/images/`+k.categories[i].image+`">
                           <div class="container">
                              <h2> <a href= /rango/category/`+ k.categories[i].slug +`>` + k.categories[i].title + `</a></h2>
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
                  </div>`
         }
         document.getElementById('archive').innerHTML = html
      }
  }
   xhr.open("GET", "/rango/get_cat", true);
   xhr.send(null);
});
let createArrayAtoZ = _ => {
   return Array 
      .apply(null, {length: 26}) 
      .map((x, i) => String.fromCharCode(65 + i));
}

let jumptoAnchor = anchor => {
   window.location.href = "#" + anchor;
}

let createNavigationList = _ => {
   const abcChars = createArrayAtoZ();
   const navigationEntries = abcChars.reduce(createDivForCharElement, ''); 
   $('#nav').append(navigationEntries);

   const lettersActive = createArrayAtoZ();
   lettersActive.forEach(letter => { 
      changeItemState(letter); 
      addListEntries(letter); 
   });
}

let changeItemState = character => {
   const characterElement = $('#nav').find('.CharacterElement[data-filter="' + character + '"]');
   $(characterElement).click(() => jumptoAnchor(character));
   characterElement.removeClass('Inactive');
}

let createDivForCharElement = (block, charToAdd) => { 
   return block + "<div id='CharacterElement' class='CharacterElement Inactive' data-filter='" + charToAdd + "'>" + charToAdd + "</div>"; 
}

let addListEntries = letter => {
   $('#AppComponent').append("<div class='AppElement' id='" + letter + "'>" + letter + "</div>");
}

