var id = document.currentScript.getAttribute('id_channel');
var page = 1;
function getContentTable(page) {

    // fetch("/api/test/").then(response => response.json()).then(data => chart.load(data));
    fetch("/content_table/"+id+"/?" + "page="+page
    ).then(response => response.text()).then(data => {
        document.getElementById("table").innerHTML = data
    });

}
getContentTable(1);