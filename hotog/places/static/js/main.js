$(document).ready(function() {
    $.get('/suggestions', {}, function(response) {
        $('#placesList').tmpl({ places: response.data }).appendTo('body');
    });
});