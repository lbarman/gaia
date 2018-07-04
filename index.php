<?php
require_once("db.php");
$db = new Db();    

if(isset($_GET['ping'])) {
    $secretToken = 'nSWXz8p7BsdY74NGNQVqJr4e';
    $secretToken2 = '';

    if(isset($_GET['token'])){
        $secretToken2 = $_GET['token'];
    }

    if($secretToken === $secretToken2){

        $timestamp = 'NULL';
        $data = '';

        if(isset($_GET['local_ts'])) {
            $timestamp = $db->escape($_GET['local_ts']);
        }
        if(isset($_GET['data'])) {
            $data = $db->escape($_GET['data']);
        }

        $db -> query("INSERT INTO `pings` (`id`, `timestamp`, `local_timestamp`, `data`) VALUES (NULL, CURRENT_TIMESTAMP, " . $timestamp .", '". $data ."');");
    }
    else
    {
        sleep(1);
        die('Invalid secret');
    }
}
?>

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Gaia</title>
        <link rel="stylesheet" type="text/css" href="sakura.css">
        <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.min.js"></script>
        <script src="chart.js"></script>
        <style>
        canvas{
            -moz-user-select: none;
            -webkit-user-select: none;
            -ms-user-select: none;
        }
        .chartjs-tooltip {
            opacity: 1;
            position: absolute;
            background: rgba(0, 0, 0, .7);
            color: white;
            border-radius: 3px;
            -webkit-transition: all .1s ease;
            transition: all .1s ease;
            pointer-events: none;
            -webkit-transform: translate(-50%, 0);
            transform: translate(-50%, 0);
            padding: 4px;
        }

        .chartjs-tooltip-key {
            display: inline-block;
            width: 10px;
            height: 10px;
        }
    </style>
    </head>
    <body>
        <h1>Gaia</h1>
        <div>
            <h3>Pings</h3>
            <div id="canvas-holder1" style="width:75%;">
                <canvas id="chart1"></canvas>
                <div class="chartjs-tooltip" id="tooltip-0"></div>
                <div class="chartjs-tooltip" id="tooltip-1"></div>
            </div>
        </div>
        <div>
            <h3>Raw Data</h3>
            <a href="#" id="toggleRawData">show/hide</a>
            <pre id="rawData"><?php
                $rows = $db -> select("SELECT * FROM `pings` ORDER BY timestamp DESC");
                var_dump($rows);
                ?>
            </pre>
        </div>
    <script type="text/javascript">
        var hidden=true;
        $('#rawData').hide();
        $('#toggleRawData').click(function() {
            if(hidden){
                $('#rawData').show(); 
                hidden = false;
            } else {
                $('#rawData').hide(); 
                hidden = true;
            }
            return false;
        });
    </script>
    <script>
        var customTooltips = function(tooltip) {
            $(this._chart.canvas).css('cursor', 'pointer');

            var positionY = this._chart.canvas.offsetTop;
            var positionX = this._chart.canvas.offsetLeft;

            $('.chartjs-tooltip').css({
                opacity: 0,
            });

            if (!tooltip || !tooltip.opacity) {
                return;
            }

            if (tooltip.dataPoints.length > 0) {
                tooltip.dataPoints.forEach(function(dataPoint) {
                    var content = [dataPoint.xLabel, dataPoint.yLabel].join(': ');
                    var $tooltip = $('#tooltip-' + dataPoint.datasetIndex);

                    $tooltip.html(content);
                    $tooltip.css({
                        opacity: 1,
                        top: positionY + dataPoint.y + 'px',
                        left: positionX + dataPoint.x + 'px',
                    });
                });
            }
        };
        var color = Chart.helpers.color;
        var lineChartData = {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            datasets: [{
                label: 'Igor',
                backgroundColor: color(window.chartColors.red).alpha(0.2).rgbString(),
                borderColor: window.chartColors.red,
                pointBackgroundColor: window.chartColors.red,
                data: [
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor()
                ]
            }, {
                label: 'Plants',
                backgroundColor: color(window.chartColors.green).alpha(0.2).rgbString(),
                borderColor: window.chartColors.green,
                pointBackgroundColor: window.chartColors.green,
                data: [
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor()
                ]
            }]
        };

        window.onload = function() {
            var chartEl = document.getElementById('chart1');
            new Chart(chartEl, {
                type: 'line',
                data: lineChartData,
                options: {
                    title: {
                        display: false,
                        text: ''
                    },
                    tooltips: {
                        enabled: false,
                        mode: 'index',
                        intersect: false,
                        custom: customTooltips
                    }
                }
            });
        };
    </script>
    </body>
</html>