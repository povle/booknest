function load_navbar(page_name) {
    $.get("/templates/navbar.html", function (value) {
        $('body').prepend(value);
        $("#nav-"+page_name).addClass("active")
    });
};

function render_books(books, template) {
    $.get(template, function (tmpl_code) {
        var tmpl = $.templates(tmpl_code);
        books.forEach(element => {
            var html = tmpl.render(element);
            $("#cards").append(html);
        });

        let script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-star-rating@4.1.2/js/star-rating.min.js';
        document.head.appendChild(script);

        let theme = document.createElement('script');
        theme.src = 'https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-star-rating@4.1.2/themes/krajee-svg/theme.js';
        document.head.appendChild(theme);
    });
};
