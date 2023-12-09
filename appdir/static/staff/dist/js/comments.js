$(".delete-real").each(function () {
    $(this).click(function () {
        id = $(this).parent().attr('id')
        console.log("id:", id)
        $.post('/staff/del_comment_real', {'id': id}).done(function (request) {
            let server = request['returnValue'];
            console.log(server);
            if (server === 200) {
                $(this).parent().parent().parent().remove();
                alert('successfully deleted')
            } else {
                console.log(server);
            }
        });
    });
});

$(".delete").each(function () {
    $(this).click(function () {
        id = $(this).parent().attr('id')
        comment = $(this).parent().parent().parent()
        console.log("id:", id)
        $.post('/staff/del_comment', {'id': id}).done(function (request) {
            let server = request['returnValue'];
            console.log(server);
            if (server === 200) {
                comment.remove();
                alert('successfully blocked')
            } else {
                console.log(server);
            }
        });
    });
});

$(".pass").each(function () {
    $(this).click(function () {
        id = $(this).parent().attr('id')
        console.log("id:", id)
        let line = $(this).parent().parent().parent();
        $.post('/staff/pass_comment', {'id': id}).done(function (request) {
            let server = request['returnValue'];
            console.log(server);
            if (server === 200) {
                line.remove()
                alert('successfully passed')
            } else {
                console.log(server);
            }
        });
    });
});