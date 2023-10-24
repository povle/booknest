function load_navbar(page_name) {
    $.get("/templates/navbar.html", function (value) {
        $('body').prepend(value);
        $("#nav-" + page_name).addClass("active")
    });
};

function get_favorites() {
    const raw = localStorage.getItem("favorites");
    if (raw !== null) { return JSON.parse(raw); };
    return [];
};

function is_favorite(id) {
    return get_favorites().includes(id);
};

function toggle_favorites(id) {
    var favorites = get_favorites();
    if (favorites.contains(id)) {
        favorites = favorites.filter(x => x!==id);
        localStorage.setItem('favorites', JSON.stringify(favorites))
        return false;
    };
    favorites.push(id);
    localStorage.setItem('favorites', JSON.stringify(favorites))
    return true;
};

function get_read_later() {
    const raw = localStorage.getItem("read_later");
    if (raw !== null) { return JSON.parse(raw); };
    return [];
};

function is_read_later(id) {
    return get_read_later().includes(id);
};

function toggle_read_later(id) {
    var read_later = get_read_later();
    if (read_later.contains(id)) {
        read_later = read_later.filter(x => x !== id);
        localStorage.setItem('read_later', JSON.stringify(read_later))
        return false;
    }
    else {
        read_later.push(id);
        localStorage.setItem('read_later', JSON.stringify(read_later));
        return true;
    };
};


function render_books(books, template, callback=null) {
    $(document).ready(function () {
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

            if (callback !== null) { callback() };
        });
    });
};
