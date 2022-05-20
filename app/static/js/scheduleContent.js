var id = document.currentScript.getAttribute('id_channel');
var id_schedule_regular = 0;
var search_like = "";

function getFormContentSchedule(id_schedule_regular=0) {
    fetch("/schedule_content_form/"+id+"/" + (id_schedule_regular ? "?id_schedule_content="+id_schedule_regular :"")
    ).then(response => response.text()).then(data => {
        document.getElementById("form_regular").innerHTML = data;
    });
}

function getFormOptions(id_schedule_regular=0) {
    fetch("/schedule_content_form_option/"+id+"/" + (search_like ? "?search="+search_like :"")
    ).then(response => response.text()).then(data => {
        document.getElementById("content_id").innerHTML = data;
    });
}

$(document).ready(function($) {
    $(".table-row").click(function() {
        console.log($(this).data("value"));
        window.document.location = $(this).data("href");
    });
});

// getFormContentSchedule();
// getFormOptions()