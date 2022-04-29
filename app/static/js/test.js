// import("./chartList.js").then(module => {
chart = getSubscribersChart('#chart');
chart2 = createBarChart('#chart_2');

// });
var days_delta = "20";
var chart_id = "0";

function updateData(channelId = "0") {
    console.log(channelId);

    // fetch("/api/test/").then(response => response.json()).then(data => chart.load(data));
    fetch("/api/statistic/channel/" + (channelId !== "0" ? `${channelId}` : "") + `?days_delta=${days_delta}`).then(response => response.json()).then(data => {
        console.log(data);
        if (channelId !== 0) {
            data.unload = chart.data().map(elemnt => elemnt.id);
            console.log(data);
            chart.load(data);
        } else {
            chart.load(data);
        }
    });

}

function selectChange(event) {
    console.log(event);

    chart_id = event.target.value;
    updateData(chart_id);

}
function selectChangeDate(event) {
    console.log(event);

    days_delta = event.target.value;
    updateData(chart_id);

}
function updateDrop() {
    // fetch("/api/test/").then(response => response.json()).then(data => chart.load(data));
    fetch("/api/statistic/channels_droplist/").then(response => response.text()).then(data => {
        console.log(data);
        document.getElementById("channel").innerHTML = data;
        chart.load(data);

    });

}

function uploadData(data = {test: "test"}) {
    fetch('/statistic/chanel_my/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(data)
    });
}

function reloadPage() {
    location.reload()
}

updateData();
updateDrop();
// setInterval(updateData, 2000);


