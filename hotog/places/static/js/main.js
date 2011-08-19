$(document).ready(function() {
    $.get('/suggestions', {}, function(response) {
        var data = response.data.map(function(v) {
            return { current: Math.round(v.current),
                     mean: Math.round(v.mean),
                     name: v.name };
        });
        $('#placesList').tmpl({ places: data }).appendTo('body');
        $('div.other-recs a.overflow').click(function() {
            $('.overflow').animate({ 'opacity': 'toggle'}, 100);
            $(this).hide();
            return false;
        });
    });
});