var chart;
var chart2;

import("./chartList.js").then(module => {
    chart = module.getSubscribersChart('#chart');
    chart2 = module.createBarChart('#chart_2');
});

function updateData(channelId = 0) {
    console.log(channelId);

    // fetch("/api/test/").then(response => response.json()).then(data => chart.load(data));
    fetch("/api/statistic/channel/" + (channelId !== 0 ? `${channelId}/` : "")).then(response => response.json()).then(data => {
        console.log(data);
        if (channelId !== 0) {

            chart.load(data)
        } else {
            chart.load(data);
        }

    });

}

function selectChange(event) {
    console.log(event);
    updateData(event.target.value)
}

function updateDrop() {
    // fetch("/api/test/").then(response => response.json()).then(data => chart.load(data));
    fetch("/statistic/channels/").then(response => response.text()).then(data => {
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


