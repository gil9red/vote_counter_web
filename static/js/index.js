$(function() {
    $('table').DataTable();
});

function add_vote(name) {
    console.log("call add_vote()");

    $.ajax({
        url: "/add-vote",
        method: "POST",  // HTTP метод, по умолчанию GET
        data: JSON.stringify({name: name}),

        contentType: "application/json",
        dataType: "json",  // тип данных загружаемых с сервера

        success: function(data) {
            console.log("success");
            console.log(data);

            // TODO:
            location.reload();
        },

        error: function(data) {
            console.log("error");
            console.log(data);
        }
    });
}

function cancel_vote(voteId) {
    console.log("call cancel_vote()");

    $.ajax({
        url: "/cancel-vote",
        method: "POST",  // HTTP метод, по умолчанию GET
        data: JSON.stringify({id: voteId}),

        contentType: "application/json",
        dataType: "json",  // тип данных загружаемых с сервера

        success: function(data) {
            console.log("success");
            console.log(data);

            // TODO:
            location.reload();
        },

        error: function(data) {
            console.log("error");
            console.log(data);
        }
    });
}