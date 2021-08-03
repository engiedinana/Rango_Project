$(document).ready(function(){
    //Bind click event handler for saving a page to favorite
    $('#saveFavorite').click(function(){
        var btn = $(this)
        pageId = btn.attr('data-pageid');
        $.get('/rango/save_favorite/', {'page_id':pageId}, function(data){
            //callback function to handle http response
            if(data == 'success') {
                //Display another button and hide the clicked one
                btn.hide();
                $('#unsaveFavorite').show();
            }       
        });      
    });
    //Bind click event handler for removing a page from favorite
    $('#unsaveFavorite').on( "click", function(){
        var btn = $(this);
        pageId = btn.attr('data-pageid');
        $.get('/rango/unsave_favorite/', {'page_id': pageId}, function(data){
            //callback function to handle http response
            if(data == 'success') {
                //Display another button and hide the clicked one
                btn.hide();
                $('#saveFavorite').show();
            }
        })
    });
});