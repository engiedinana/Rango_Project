/**
 * This function is for finding the value of csrf token and include it in jquery for
 * ajax post requests
 * @param {name of the cookie} name 
 * @returns the cookie value
 */
function getCookie(name) {
    var cookieValue = null;
    if(document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i=0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i])
            if(cookie.substring(0, name.length+1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * 
 * @param {object} elm document object or a button 
 * @param {string} action string to figure out user wants to save or unsave the page
 * to favorites
 * 
 * This function take in a document object, a button and handles click on it
 * Upon click a ajax get request is fired and interactions with 
 * DB are performed . Finally the UI reflects this upon receiving success response 
 * by displaying another button 
 */

function saveUnsavePage(elm, action) {
    //#Holds the id of the button to toggle
    var id_str = '';
    //Bind click event handler for saving a page to favorite
    $("#"+elm.id).click(function(){ 
            if (action == "save") {
                //Url to send the post request to 
                var url = '/rango/save_favorite/';
                //Get only the id or loop counter from element id
                id_str = '#unsaveFavorite' + elm.id.match(/\d+$/);
            }
            else if(action == "unsave") {
                //Url to send the post request to 
                var url = '/rango/unsave_favorite/';
                //Get only the id or loop counter from element id
                id_str = '#saveFavorite' + elm.id.match(/\d+$/);
            }
            else{
                console.log("should not reach here")
            }
            //store the current element clicked in a variable
            var btn = $(this);
            //Get the unique page id to interact with the DB
            pageId = btn.attr('data-pageid');
            //Get csrf token
            var csrftoken = getCookie('csrftoken');

            //Ajax post request to talk to the view save or unsave and interact with DB
            $.ajax({
                url: url,
                type: "POST",
                data:{
                    csrfmiddlewaretoken : csrftoken,
                    page_id:pageId
                },
                //callback function to handle post success
                success: function(json) {
                    if(json.response === 1) { //Just double checking success
                        btn.hide();                        
                        //Show corresponding button
                        $(id_str).show();     
                    }
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status+": "+xhr.responseText)
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
        if(elm.id.startsWith("save")) {
          saveUnsavePage(elm, "save");  
        }  
        else if(elm.id.startsWith("unsave")) {
            saveUnsavePage(elm, "unsave");
        }
    });

    //For each button decide which handler to add dynamically from user profile page 
    // either add or remove from favorites list
    favListButtons.each(function(index, elm) {
        if(elm.id.startsWith("save")) {
            saveUnsavePage(elm, "save"); 
        }  
        else if(elm.id.startsWith("unsave")) {
            saveUnsavePage(elm, "unsave");
        }
    });
});

