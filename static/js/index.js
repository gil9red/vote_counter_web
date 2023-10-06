$.noty.defaults.theme = 'defaultTheme';
$.noty.defaults.layout = 'bottomRight';
$.noty.defaults.timeout = 6000;


function getDiffInDays(date_1, date_2) {
    let difference = date_1.getTime() - date_2.getTime();
    return Math.floor(difference / (1000 * 3600 * 24));
}

function date_render(data, type, row, meta) {
    if (data == null) {
        return null;
    }

    if (type === 'display' || type === 'filter') {
        return data.display;
    }
    return data.timestamp;
}

function ajaxSuccess(data) {
    console.log("success");
    console.log(data);

    window.tableCounter.ajax.reload();
    window.tableAllVotes.ajax.reload(setDaysWithoutIncident);
}

function ajaxError(data) {
    console.log("error");
    console.log(data);
}

function showError(text) {
    noty({
        text: text,
        type: 'error',
    });
}

function add_vote(name) {
    console.log("call add_vote()");

    $.ajax({
        url: "/api/add-vote",
        method: "POST",  // HTTP метод, по умолчанию GET
        data: JSON.stringify({name: name}),

        contentType: "application/json",
        dataType: "json",  // тип данных загружаемых с сервера

        success: ajaxSuccess,
        error: ajaxError,
    });
}

function cancel_vote(voteId) {
    console.log("call cancel_vote()");

    $.ajax({
        url: "/api/cancel-vote",
        method: "POST",  // HTTP метод, по умолчанию GET
        data: JSON.stringify({id: voteId}),

        contentType: "application/json",
        dataType: "json",  // тип данных загружаемых с сервера

        success: ajaxSuccess,
        error: ajaxError,
    });
}

function setDaysWithoutIncident() {
    // Берем первую строку без даты отмены
    let row = window.tableAllVotes
        .rows()
        .data()
        .sort((data1, data2) => {
            // Сортировка от большего к меньшему
            return data2.id - data1.id;
        })
        .filter((value, index) => {
            return value.cancel_date == null;
        })
        .shift()
    ;
    if (row == null) {
        return;
    }

    let now = new Date();
    let appendDate = new Date(row.append_date.timestamp * 1000);

    let daysWithoutIncident = getDiffInDays(now, appendDate);
    $(".days-without-incident").text(daysWithoutIncident);
}

$(function() {
    $("#modelLogin form").submit(function() {
        let thisForm = this;

        let url = $(this).attr("action");
        let method = $(this).attr("method");
        if (method === undefined) {
            method = "get";
        }

        let data = $(this).serialize();

        $.ajax({
            url: url,
            method: method,  // HTTP метод, по умолчанию GET
            data: data,
            dataType: "json",  // Тип данных загружаемых с сервера
            success: function(data) {
                if (data.ok) {
                    // Очищение полей формы
                    thisForm.reset();
                    location.reload();
                } else {
                    showError(data.error);
                }
            },
            error: data => showError('Неизвестная ошибка при логине'),
        });

        return false;
    });

    window.tableCounter = $('#table-counter').DataTable({
        ajax: {
            url: "/api/counter",
            dataSrc: "", // Придет список, а не словарь
        },
        columns: [
            { data: 'name' },
            { data: 'counter' },
            {
                data: 'name',
                render: (data, type, row) => {
                    return `
                        <button
                            type="button"
                            class="btn btn-primary btn-sm"
                            onclick="add_vote('${data}')"
                            ${row.append_disabled ? 'disabled' : ''}
                        >
                            +
                        </button>
                    `
                },
                searchable: false,
                orderable: false,
                width: "50px",
            },
        ],
        order: [[1, 'desc']],  // Сортировка по количеству
        lengthMenu: [
            [5, 10, 25, 50, -1],
            [5, 10, 25, 50, "все"],
        ],
        pageLength: -1,
        language: DATATABLES_LANG_RU,
    });

    window.tableAllVotes = $('#table-all-votes').DataTable({
        ajax: {
            url: "/api/all",
            dataSrc: "", // Придет список, а не словарь
        },
        columns: [
            { data: 'id' },
            { data: 'name' },
            { data: 'sender_login' },
            {
                data: "append_date",
                render: date_render,
            },
            {
                data: "cancel_date",
                render: date_render,
            },
            {
                data: null,
                render: (data, type, row) => {
                    return `
                        <button
                            type="button"
                            class="btn btn-danger btn-sm"
                            onclick="cancel_vote('${row.id}')"
                            ${row.deletion_disabled ? 'disabled' : ''}
                        >
                            -
                        </button>
                    `
                },
                searchable: false,
                orderable: false,
                width: "50px",
            },
        ],
        order: [[0, 'desc']],  // Сортировка по ид
        language: DATATABLES_LANG_RU,
        lengthMenu: [
            [5, 10, 25, 50, -1],
            [5, 10, 25, 50, "все"],
        ],
        createdRow: (row, data, dataIndex) => {
            // Выделение серым цветом строки с отмененным голосом
            if (data.cancel_date != null) {
                $(row).addClass('text-secondary');
            }
        },
        initComplete: function () {
            setDaysWithoutIncident();
        },
    });
});
