$(document).ready(function() {
    $.get('/suggestions', {}, function(response) {
        $('#placesList').tmpl({ places: response.data }).appendTo('body');
        $('div.other-recs a.overflow').click(function() {
            $('.overflow').show();
            $(this).hide();
            return false;
        });
    });
});