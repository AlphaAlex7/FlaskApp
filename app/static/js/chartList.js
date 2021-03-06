function getSubscribersChart(divId) {
    return c3.generate({
        bindto: divId,
        size: {
            height: 400,
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
            ]
        },
        axis: {
            y: {
                label: {
                    text: 'X',
                    position: 'outer-middle'
                },
                show: false,
            },
            x: {
                label: {
                    text: "",
                    position: 'outer-middle'
                },
                show: false,
            }
        }, legend: {
            show: false
        }

    });
}

function getSplineWithOutAxis(divId, labelY = "") {
    return c3.generate({
        bindto: divId,
        data: {
            columns: [],
            type: 'bar',
            labels: {
                format: function (v, id, i, j) {
                    return id;
                }
            }
        },
        size: {
            height: 200,
        },
        axis: {
            y: {
                label: {
                    text: labelY,
                    position: 'outer-middle'
                },
                show: labelY === "" ? false : true,
            },
            x: {
                label: {
                    text: "",
                    position: 'outer-middle'
                },
                show: false,
            }
        }, legend: {
            show: false
        },
        bar: {
            width: {
                ratio: 1// this makes bar width 50% of length between ticks
            }
            // or
            //width: 100 // this makes bar width 100px
        }

    });
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
