function load_navbar(page_name) {
    $.get("/templates/navbar.html", function (value) {
        $('body').prepend(value);
        $("#nav-" + page_name).addClass("active")
    });
};

function get_arr_from_storage(name) {
    const raw = localStorage.getItem(name);
    if (raw !== null) { return JSON.parse(raw); };
    return [];
};

function toggle_in_storage(id, name) {
    let arr = get_arr_from_storage(name);
    if (arr.includes(id)) {
        arr = arr.filter(x => x !== id);
        localStorage.setItem(name, JSON.stringify(arr))
        return false;
    };
    arr.push(id);
    localStorage.setItem(name, JSON.stringify(arr))
    return true;
};

function set_button(id, type, value) {
    let btn = $('#btn-' + type + '-' + id);
    if (value) {
        btn.removeClass('btn-outline-primary');
        btn.addClass('btn-primary');
    }
    else {
        btn.addClass('btn-outline-primary');
        btn.removeClass('btn-primary');
    };
}

function toggle_button(id, type) {
    let result = toggle_in_storage(id, type);
    set_button(id, type, result);
    return result;
};


function render_books(books, template, callback=null) {
    $(document).ready(function () {
        $.get(template, function (tmpl_code) {
            const favorites = get_arr_from_storage('favorites');
            const read_later = get_arr_from_storage('read_later');
            var tmpl = $.templates(tmpl_code);
            books.forEach(book => {
                var html = tmpl.render(book);
                $("#cards").append(html);
                set_button(book.id, 'favorites', favorites.includes(book.id));
                set_button(book.id, 'read_later', read_later.includes(book.id));
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
