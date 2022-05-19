var id = document.currentScript.getAttribute('id_channel');
var id_schedule_regular = 0;
function getFormRegular(id_schedule_regular=0) {
    fetch("/schedule_regular_form/"+id+"/" + (id_schedule_regular ? "?id_schedule_regular="+id_schedule_regular :"")
    ).then(response => response.text()).then(data => {
        document.getElementById("form_regular").innerHTML = data;
    });

}
$(document).ready(function($) {
    $(".table-row").click(function() {
        console.log($(this).data("value"))
        getFormRegular($(this).data("value"));
    });
});

getFormRegular()