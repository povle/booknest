$.get("/templates/navbar.html", function (value) {
    $('body').prepend(value);
});
