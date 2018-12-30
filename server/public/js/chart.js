var PRECISION = 24 * 3600

function meanArray(array) {
    var acc = 0
    for(var i=0; i<array.length; i++){
        acc += array[i]
    }
    return Math.round(acc * 10 / array.length) / 10
}

function roundTo(x) {
    return Math.floor(x / PRECISION) * PRECISION
}

function groupByLabelAndSum(rawData, labels, operation) {
    var hashMap = {}
    for (var property in rawData) {
        if (rawData.hasOwnProperty(property)) {

            t = roundTo(Number(property))
            if(operation == "sum") {
                if (hashMap[t] == undefined) {
                    hashMap[t] = 0
                }
                hashMap[t] += Number(rawData[property])
            } else if(operation == "mean") {
                if (hashMap[t] == undefined) {
                    hashMap[t] = [[], [], [], []] //t1, humidity, t2, t3
                }
                hashMap[t][0].push(Number(rawData[property][0]))
                hashMap[t][1].push(Number(rawData[property][1]))
                hashMap[t][2].push(Number(rawData[property][2]))
                hashMap[t][3].push(Number(rawData[property][3]))
            }
        }
    }

    if(operation == "mean") {
        for (var key in hashMap) {
            if (hashMap.hasOwnProperty(key)) {
                
                hashMap[key][0] = meanArray(hashMap[key][0])
                hashMap[key][1] = meanArray(hashMap[key][1])
                hashMap[key][2] = meanArray(hashMap[key][2])
                hashMap[key][3] = meanArray(hashMap[key][3])
            }
        }
    }

    if (labels == undefined) {
        // we compute our own labels
        labels = []
        var dataset = []
        for (var property in hashMap) {
            if (hashMap.hasOwnProperty(property)) {
                t = new Date(1000 * Number(property))
                labels.push(t)
                dataset.push({
                    t: t,
                    y: hashMap[property]
                });
            }
        }
        return [labels, dataset]
    } else {
        // we use the given labels
        var dataset = []
        for (i = 0; i < labels.length; i++) {

            t = labels[i]
            timestamp = t.getTime() / 1000

            if (hashMap.hasOwnProperty(timestamp)) {
                if(operation == "sum") {
                    dataset.push({
                        t: t,
                        y: 1
                    });
                } else {
                    dataset.push({
                        t: t,
                        y: hashMap[timestamp]
                    });
                }
            } else {
                dataset.push({
                    t: t,
                    y: 0
                });
            }
        }
        return [labels, dataset]
    }
}

var pingsLabelsAndVals = groupByLabelAndSum(data_status, undefined, "sum");
var tempLabelsAndVals = groupByLabelAndSum(data_temps, pingsLabelsAndVals[0], "mean");
var feedingLabelsAndVals = groupByLabelAndSum(data_feeding, pingsLabelsAndVals[0], "sum");
var wateringLabelsAndVals = groupByLabelAndSum(data_watering, pingsLabelsAndVals[0], "sum");

// nice labels
var labels = [];
for (i = 0; i < pingsLabelsAndVals[0].length; i++) {
    d = pingsLabelsAndVals[0][i];
    labels.push(d.getDate() + "/" + (d.getMonth() + 1) + " " + d.getHours()+"h");
}

// make the important info (watering, feeding) stand out by scaling them with respect to max pings
maxValue = 0
for (i = 0; i < pingsLabelsAndVals[1].length; i++) {
    maxValue = Math.max(maxValue, pingsLabelsAndVals[1][i].y)
}
maxValue = -maxValue
for (i = 0; i < feedingLabelsAndVals[1].length; i++) {
    feedingLabelsAndVals[1][i].y = maxValue * feedingLabelsAndVals[1][i].y
}
for (i = 0; i < wateringLabelsAndVals[1].length; i++) {
    wateringLabelsAndVals[1][i].y = maxValue * wateringLabelsAndVals[1][i].y
}

/*
// print interesting info
igorUnprocessedData = toDataset(data_feeding, undefined);
str = "# igor fed:" + "\n"
for (var property in data_feeding) {
    if (data_feeding.hasOwnProperty(property)) {
        t = new Date(1000 * Number(property))
        str += t.toUTCString().replace(" GMT", "") + "\n"
    }
}
str += "\n"
str += "# plants watered:" + "\n"
for (var property in data_watering) {
    if (data_watering.hasOwnProperty(property)) {
        t = new Date(1000 * Number(property))
        str += t.toUTCString().replace(" GMT", "") + "\n"
    }
}

$('#graphData').html(str)
*/

// plot
var red = '#eb8787'
var green = 'rgb(75, 192, 192)'
var blue = 'rgb(54, 162, 235)'
var purple = '#c86eff'

var color = Chart.helpers.color;
var barChartData = {
    labels: labels,
    datasets: [{
        label: 'Ping',
        backgroundColor: color(green).alpha(0.2).rgbString(),
        borderColor: green,
        pointBackgroundColor: green,
        data: pingsLabelsAndVals[1],
    }, {
        label: 'Feeding',
        backgroundColor: color(red).alpha(0.2).rgbString(),
        borderColor: red,
        pointBackgroundColor: red,
        data: feedingLabelsAndVals[1],
    }, {
        label: 'Watering',
        backgroundColor: color(blue).alpha(0.2).rgbString(),
        borderColor: blue,
        pointBackgroundColor: blue,
        data: wateringLabelsAndVals[1],
    }]
};

temp1Values = []
humidityValues = []
temp2Values = []
temp3Values = []

for (i = 0; i < tempLabelsAndVals[1].length; i++) {
    temp1Values.push(tempLabelsAndVals[1][i]['y'][0])
    humidityValues.push(tempLabelsAndVals[1][i]['y'][1])
    temp2Values.push(tempLabelsAndVals[1][i]['y'][2])
    temp3Values.push(tempLabelsAndVals[1][i]['y'][3])
}
var lineChartData = {
    labels: labels,
    datasets: [{
        label: 'Temperature',
        backgroundColor: color(red).alpha(0.1).rgbString(),
        borderColor: color(red).alpha(0.5).rgbString(),
        data: temp1Values,
    }, {
        label: 'Humidity',
        backgroundColor: color(blue).alpha(0.1).rgbString(),
        borderColor: color(blue).alpha(0.5).rgbString(),
        data: humidityValues,
    },{
        label: 'Temperature 2',
        backgroundColor: color(green).alpha(0.1).rgbString(),
        borderColor: color(green).alpha(0.5).rgbString(),
        data: temp2Values,
    },{
        label: 'Temperature 3',
        backgroundColor: color(purple).alpha(0.1).rgbString(),
        borderColor: color(purple).alpha(0.5).rgbString(),
        data: temp3Values,
    }]
};

window.onload = function() {
    new Chart(document.getElementById('chart1'), {
        type: 'bar',
        data: barChartData,
        options: {
            title: {
                display: false,
                text: ''
            },
        },
    });
    new Chart(document.getElementById('chart2'), {
        type: 'line',
        data: lineChartData,
        options: {
            title: {
                display: false,
                text: ''
            },
        },
    });
};
