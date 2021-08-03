$(document).ready(function(){
    var buttons = $("ul").find('button');
    var id_str = '';
    var pageId = null;

    buttons.each(function(index, elm) {
        if(elm.id.startsWith('save')) {
            //Bind click event handler for saving a page to favorite
            $('#'+elm.id).click(function(){
                console.log("Saving");
                    var btn = $(this);
                    pageId = btn.attr('data-pageid');
                    $.get('/rango/save_favorite/', {'page_id':pageId}, function(data){
                        //callback function to handle http response
                        if(data == 'success') {
                            //Display another button and hide the clicked one
                            btn.hide();
                            id_str = '#unsaveFavorite' + elm.id.match(/\d+$/);
                            $(id_str).show();
                        }       
                    });     
                });
          }  
        else if(elm.id.startsWith('unsave')) {
             //Bind click event handler for removing a page from favorite
            $('#'+elm.id).click(function() {
                console.log("Unsaving");
                var btn = $(this);
                pageId = btn.attr('data-pageid');
                $.get('/rango/unsave_favorite/', {'page_id': pageId}, function(data){
                    //callback function to handle http response
                    if(data == 'success') {
                        //Display another button and hide the clicked one
                        btn.hide();
                        id_str = '#saveFavorite' + elm.id.match(/\d+$/);
                        $(id_str).show();
                    }
                });
            });
        }
    })
});