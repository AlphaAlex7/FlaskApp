var colors = ['red', 'blue', 'green', 'yellow', 'green', 'red'];
var chart = getSubscribersChart('#chart');
var chart2 = getSplineWithOutAxis('#chart_2');
var chart3 = getSplineWithOutAxis('#chart_3');
var chart4 = getSplineWithOutAxis('#chart_4');
var elements_colors;
var days_delta = "20";
var channel_id = "0";

function strTohex(string) {
    var str = string;
    var hex = '';
    for (var i = 0; i < str.length; i++) {
        hex += '' + str.charCodeAt(i).toString(10);
    }
    return hex;
}

function chart_colors() {
    elements_colors = {};
    chart.data().forEach((elemnt, index) => elements_colors[elemnt.id] = colors[index]);
    return elements_colors
}

function updateDataMainChart() {
    console.log(channel_id);
    // fetch("/api/test/").then(response => response.json()).then(data => chart.load(data));
    fetch("/api/statistic/channel-main-chart/?" +
        `days_delta=${days_delta}` +
        (channel_id !== "0" ? `&channel_id=${channel_id}` : "")
    ).then(response => response.json()).then(data => {
        if (channel_id !== 0) {
            console.log(data)
            data.unload = chart.data().map(elemnt => elemnt.id);
            chart.load(data);
        } else {
            chart.load(data);
        }
        chart.axis.range({max: {x: Date.now()}, min: {x: Date.now() - ((days_delta - 1) * 24 * 3600 * 1000)}});
    });

}

function updateAverageFollowersChart() {
    console.log(channel_id);
    // fetch("/api/test/").then(response => response.json()).then(data => chart.load(data));
    fetch("/api/statistic/channel-average-subscribers/?" +
        (channel_id !== "0" ? `&channel_id=${channel_id}` : "")
    ).then(response => response.json()).then(data => {
        if (channel_id !== 0) {
            data.unload = chart2.data().map(elemnt => elemnt.id);
            chart2.load(data);
        } else {
            chart2.load(data);
        }
    });

}

function selectChange(event) {
    console.log(event);

    channel_id = event.target.value;
    updateAverageFollowersChart();
    updateDataMainChart();
}

function selectChangeDate(event) {
    console.log(event);

    days_delta = event.target.value;

    updateDataMainChart();


}

// function updateDrop() {
//     // fetch("/api/test/").then(response => response.json()).then(data => chart.load(data));
//     fetch("/api/statistic/channels_droplist/").then(response => response.text()).then(data => {
//         console.log(data);
//         document.getElementById("channel").innerHTML = data;
//         chart.load(data);
//
//     });
//
// }

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

updateDataMainChart();
updateAverageFollowersChart();
// updateDrop();
// setInterval(updateData, 2000);


