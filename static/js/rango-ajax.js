$(document).ready(function(){
    $('#saveFavorite').click(function(){
        var btn = $(this)
        pageId = btn.attr('data-pageid');
        $.get('/rango/save_favorite/', {'page_id':pageId}, function(data){
            if(data == 'success') {
                btn.hide();
                $('#unsaveFavorite').show();
            }
        })      
    });

    $('#unsaveFavorite').click(function(){
        var btn = $(this)
        pageId = btn.attr('data-pageid');
        $.get('/rango/unsave_favorite/', {'page_id': pageId}, function(data){
            btn.hide();
            $('#saveFavorite').show();
        })
    });
});