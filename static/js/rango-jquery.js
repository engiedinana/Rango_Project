$(document).ready(function() {
    var elm = $('#id_favorite');
    if(elm != null) {
        elm.removeAttr('required');
        //elm.hide();
    }
});