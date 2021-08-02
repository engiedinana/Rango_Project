$(document).ready(function(){
    $('#saveFavorite').on( "click",function(){
        var btn = $(this)
        if(btn !== null) {
            pageId = btn.attr('data-pageid');
            $.get('/rango/save_favorite/', {'page_id':pageId}, function(data){
                if(data == 'success') {
                    btn.hide();
                    $('#unsaveFavorite').show();
                }       
        });
    }      
    });

    $('#unsaveFavorite').on( "click", function(){
        var btn = $(this)
        if(btn !== null) {
            pageId = btn.attr('data-pageid');
            $.get('/rango/unsave_favorite/', {'page_id': pageId}, function(data){
                if(data == 'success') {
                    btn.hide();
                    $('#saveFavorite').show();
                }
            })
        }
    });
});