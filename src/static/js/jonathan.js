$(function() {
    $('a.file').click(function(event) {
        //event.preventDefault();
        target = $(event.currentTarget);
        localStorage[target.attr('href')] = new Date().format('d/mm/yy HH:MM');
    });

    $('a.file').each(function(index, item) {
        if(localStorage[$(item).attr('href')]) {
            $(item).parent('li').find('span.last_view_date').text("Last view: "+localStorage[$(item).attr('href')]).show();
        }
    });
});
