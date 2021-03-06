var mainChart = getSubscribersChart('#chart');
var averageFollowers = getSplineWithOutAxis('#chart_2', labelY = "Подписчики");
var averageContent = getSplineWithOutAxis('#chart_3', labelY = "Просмотры");
var days_delta = "20";
var channel_id = "0";


function updateDataMainChart() {
    console.log(channel_id);
    // fetch("/api/test/").then(response => response.json()).then(data => chart.load(data));
    fetch("/api_chart/channel-main-chart/?" +
          `days_delta=${days_delta}` +
          (channel_id !== "0" ? `&channel_id=${channel_id}` : "")
    ).then(response => response.json()
    ).then(data => {
        if (channel_id !== 0) {
            data.unload = mainChart.data().map(elemnt => elemnt.id);
            mainChart.load(data);
        } else {
            mainChart.load(data);
        }
        mainChart.axis.range({max: {x: Date.now()}, min: {x: Date.now() - ((days_delta) * 24 * 3600 * 1000)}});
    });

}

function updateAverageFollowersChart() {
    console.log(channel_id);
    // fetch("/api/test/").then(response => response.json()).then(data => chart.load(data));
    fetch("/api_chart/channel-average-subscribers/?" + `days_delta=${days_delta}`
    ).then(response => response.json()
    ).then(data => {
        if (channel_id !== 0) {
            data.unload = averageFollowers.data().map(elemnt => elemnt.id);
            averageFollowers.load(data);
        } else {
            averageFollowers.load(data);
        }
    });

}

function updateAverageContentChart() {
    console.log(channel_id);
    // fetch("/api/test/").then(response => response.json()).then(data => chart.load(data));
    fetch("/api_chart/channel-average-content-views/?" +
        (channel_id !== "0" ? `&channel_id=${channel_id}` : "")
    ).then(response => response.json()).then(data => {
        if (channel_id !== 0) {
            data.unload = averageContent.data().map(elemnt => elemnt.id);
            averageContent.load(data);
        } else {
            averageContent.load(data);
        }
    });

}

function selectChange(event) {
    channel_id = event.target.attributes.value.value;
    updateDataMainChart();
}

function selectChangeDate(event) {
    days_delta = event.target.attributes.value.value;
    updateDataMainChart();


}

updateDataMainChart();
updateAverageFollowersChart();
updateAverageContentChart();


