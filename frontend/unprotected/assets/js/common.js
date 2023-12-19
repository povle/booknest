function get_user() {
    var jwt = document.cookie.split('; ').find(row => row.startsWith('Authorization')).split('=')[1].substring(7);
    var user = JSON.parse(atob(jwt.split('.')[1]));
    return user;
}

function load_navbar(page_name, q="") {
    var user = get_user();
    if (user.is_admin) {
        var template = "/templates/navbar_admin.html";
    }
    else {
        var template = "/templates/navbar.html";
    };
    $.get(template, function (value) {
        var tmpl = $.templates(value);
        var html = tmpl.render({username: user.username || "Гость"});
        $('body').prepend(html);
        $("#nav-" + page_name).addClass("active")
        $('#searchInput').val(q);
    });
};

function load_navbar_guest(page_name) {
    $.get("/templates/navbar_guest.html", function (value) {
        $('body').prepend(value);
        $("#nav-" + page_name).addClass("active")
    });
};

function get_arr_from_storage(name) {
    var result = null;
    $.ajax({
        url: '/api/' + name,
        type: 'get',
        dataType: 'json',
        async: false,
        success: function (data) {
            result = data;
        }
    });
    return result;
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
    let user = get_user();
    let btn = $('#btn-' + type + '-' + id);
    if (user.is_admin) {
        btn.addClass('disabled');
        return;
    };
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
    var res = null;
    $.ajax({
        url: '/api/' + type + '/toggle',
        type: "POST",
        data: JSON.stringify({ book_id: id }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        async: false,
        success: function (result) {
            set_button(id, type, result);
            res = result;
        }
    });
    return res;
};


function render_books(books, template, callback=null) {
    books.forEach(book => {
        book.id = book._id;
    });
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
