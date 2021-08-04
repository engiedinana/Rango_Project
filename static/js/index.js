window.addEventListener('load',  function() {
   document.getElementById("greeting").innerHTML = "BAKRAHKO KOLOKO"
   var xhr = new XMLHttpRequest();
   var k;
   xhr.onreadystatechange = function() {
      if (xhr.readyState == XMLHttpRequest.DONE) {
         k = xhr.responseText
          alert(k);
          console.log(k)
      }
  }
   xhr.open("GET", "get_cat", true);
   xhr.send(null);
   
});
