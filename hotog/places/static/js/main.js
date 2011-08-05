$(document).ready(function() {
    $.get('/suggestions', {}, function(response) {
        $.each(response.data, function(i, v) {
            console.log(i, v);
        });
    });
});