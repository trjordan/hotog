$(document).ready(function() {
    $.get('/suggestions', {}, function(response) {
        $('#placesList').tmpl({ places: response.data }).appendTo('body');
        $('div.other-recs a.overflow').click(function() {
            $('.overflow').animate({ 'opacity': 'toggle'}, 100);
            $(this).hide();
            return false;
        });
    });
});