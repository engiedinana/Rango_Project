function saveLink(elm) {
    console.log(elm);
    //#Holds the id of the button to toggle
    var id_str = '';
    //Bind click event handler for saving a page to favorite
    $("#"+elm.id).click(function(){
            //store the current element clicked in a variable
            var btn = $(this);
            //Get the unique page id to interact with the DB
            pageId = btn.attr('data-pageid');
            $.get('/rango/save_favorite/', {'page_id':pageId}, function(data){
                //callback function to handle http response
                if(data === 'success') {
                    //Display another button and hide the clicked one
                    btn.hide();
                    //Get only the id or loop counter from element id
                    id_str = '#unsaveFavorite' + elm.id.match(/\d+$/);
                    //Show corresponding button
                    $(id_str).show();
                }       
            });     
        });
}

function removeLink(elm) {
     //#Holds the id of the button to toggle
     var id_str = '';
    //Bind click event handler for removing a page from favorite
    $('#'+elm.id).click(function() {
        //store the current element clicked in a variable
        var btn = $(this);
        //Get the unique page id to interact with DB
        pageId = btn.attr('data-pageid');
        //ajax get request to remove page from DB
        $.get('/rango/unsave_favorite/', {'page_id': pageId}, function(data){
        //callback function to handle http response
        if(data === 'success') {
        //Display another button and hide the clicked one
            btn.hide();
            //Get only the id or loop counter from element id
            id_str = '#saveFavorite' + elm.id.match(/\d+$/);
            //Show corresponding button
            $(id_str).show();
        }
    });
});
}

$(document).ready(function(){
    //Fetch all buttons and add a click handler to all 
    var buttons = $("ul#parentPage").find('button');
    var favListButtons = $("ul#favListParent").find('button');
    $('[data-toggle="tooltip"]').tooltip();
    $('.hamada').tooltip();
    
    //For each button decide which handler to add , either add or remove from favorites list
    buttons.each(function(index, elm) {
        if(elm.id.startsWith('save')) {
          saveLink(elm);  
        }  
        else if(elm.id.startsWith('unsave')) {
            removeLink(elm);
        }
    });

    //For each button decide which handler to add dynamically from user profile page 
    // either add or remove from favorites list
    favListButtons.each(function(index, elm) {
        if(elm.id.startsWith('save')) {
          saveLink(elm);  
        }  
        else if(elm.id.startsWith('unsave')) {
            removeLink(elm);
        }
    });
});

