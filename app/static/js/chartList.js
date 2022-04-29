function getSubscribersChart(divId) {
    return c3.generate({
        bindto: divId,
        size: {
            height: 500,
        },
        data: {
            xFormat: '%Y-%m-%d %H:%M:%S',
            columns: [],
            type: 'spline',
        },
        axis: {
            y: {
                label: { // ADD
                    text: 'Подписчики'
                }
            },
            x: {
                max: Date.now(),
                label: { // ADD
                    text: "Дата"
                },
                type: 'timeseries',
                tick: {
                    count: 5,
                    format: '%Y-%m-%d'
                }
            }

        },
        legend: {
            show: false
        }
    })
}

function getTestChart(divId) {
    return c3.generate({
        bindto: divId,
        data: {
            columns: [
                ['data1', 30, 200, 1000, 400, 150, 250],
                ['data2', 50, 20, 10, 40, 15, 25]
            ],
            type: 'spline',
        },
        axis: {
            y: {
                label: {
                    text: 'X',
                    position: 'outer-middle'
                }
            },
            x: {
                label: {
                    text: "",
                    position: 'outer-middle'
                }
            }
        }

    })
}

function createBarChart(divId) {
    return c3.generate({

        bindto: divId,
        data: {
            columns: [
                ['data1', 30, 200, 1000, 400, 150, 250]
            ],
            type: 'bar'
        },
        bar: {
            width: {
                ratio: 0.9// this makes bar width 50% of length between ticks
            }
            // or
            //width: 100 // this makes bar width 100px
        }
    });


}
