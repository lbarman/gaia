<?php
require_once("db.php");

$DURATION_TO_COVER_HOURS = 72;
$BAR_DURATION_HOURS = 6;

function formatTime($t){
    $seconds = strtotime($t);
    return date('H:i:s, d.m.Y', $seconds);
}

function handleRaspberryConnection($db){
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

            $s = "INSERT INTO `pings` (`id`, `timestamp`, `local_timestamp`, `data`) VALUES (NULL, CURRENT_TIMESTAMP, '" . $timestamp ."', '". $data ."');";
            $db->query($s);

            die("OK");
        }
        else
        {
            sleep(1);
            die('Invalid secret');
        }
    }
}

$db = new Db();                 # connect to DB
handleRaspberryConnection($db); # check if connection is a ping from the Raspberry

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
            <div id="canvas-holder1" style="width:100%;">
                <canvas id="chart1"></canvas>
            </div>

        <div>
            <?php

                $rows = $db->select("SELECT id,timestamp,local_timestamp,data FROM `pings` ORDER BY timestamp DESC LIMIT 1000");
                
                $toInt = function($s) {
                    return (int)$s;
                };

                $t = time();
                $t = 3600 * ceil($t / 3600); #round to the next hour

                $xAxis = [];
                $xLabels = [];

                $numberOfXPoints = ceil($DURATION_TO_COVER_HOURS / $BAR_DURATION_HOURS);

                for($h=$numberOfXPoints; $h > 0; $h--){
                    $startTime = $t - 60 * 60 * $h * $BAR_DURATION_HOURS;
                    $endTime = $t - 60 * 60 * ($h - 1) * $BAR_DURATION_HOURS;
                    $xAxis[] = array($startTime, $endTime);
                    $xLabels[] = date("d/m h\\h", $startTime);
                }

                //print xLabels for js
                echo '<script>var xLabels = [];'."\n";
                for($i = 0 ; $i < count($xLabels); $i++){

                    echo 'xLabels['.$i.'] = \''.$xLabels[$i].'\';'."\n";
                }
                echo '</script>';

                //for each xTick, check if we have something to print 
                $igorPing = array();
                $igorFed = array();
                $igorPingTooltip = array();
                $igorFedTooltip = array();
                for($i = 0 ; $i < count($xAxis); $i++){
                    $igorPing[$i] = 0;
                    $igorFed[$i] = 0;

                    foreach($rows as $row) {
                        $str = $row['local_timestamp'];
                        $ts = (int)strtotime($row['local_timestamp']);
                        
                        $data = base64_decode($row['data']);
                        if($ts >= $xAxis[$i][0] && $ts < $xAxis[$i][1]){
                            if($data == "Feeded"){
                                $igorFed[$i] -= 10;
                                $igorFedTooltip[$xLabels[$i]] = $row['local_timestamp'];
                            } else {
                                $igorPing[$i] += 1;
                            }
                        }
                    }
                }

                //print igorFed for js
                echo '<script>var igorFed = [];'."\n";
                for($i = 0 ; $i < count($igorFed); $i++){

                    echo 'igorFed['.$i.'] = \''.$igorFed[$i].'\';'."\n";
                }

                //print igorPing for js
                echo 'var igorPing = [];'."\n";
                for($i = 0 ; $i < count($igorPing); $i++){

                    echo 'igorPing['.$i.'] = \''.$igorPing[$i].'\';'."\n";
                }

                //print igorFedTooltip for js
                echo 'var igorFedTooltip = [];'."\n";
                foreach($igorFedTooltip as $k => $v){

                    echo 'igorFedTooltip[\''.$k.'\'] = \''.$v.'\';'."\n";
                }
                echo '</script>';

                ?>
        </div>
        </div>
        <div>
            <h3>Data</h3>
            <?php

                $rows = $db->select("SELECT id,timestamp,local_timestamp,data FROM `pings` ORDER BY timestamp DESC LIMIT 1000");
                foreach($rows as $row) {
                    echo '<div>';
                    echo '<h5>[#'.$row['id'].'] '.
                        formatTime($row['local_timestamp']).'</h5>';
                    echo 'Created at '.formatTime($row['timestamp']);
                    echo '<pre>'.base64_decode($row['data']).'</pre>';
                    echo '</div>';
                }
                ?>
        </div>
    <script type="text/javascript">
        /*
        var hidden=true;
        $('.rawData').hide();
        $('#toggleRawData').click(function() {
            if(hidden){
                $('.rawData').show(); 
                hidden = false;
            } else {
                $('.rawData').hide(); 
                hidden = true;
            }
            return false;
        });
        */
    </script>
    <script>
        var color = Chart.helpers.color;
        var lineChartData = {
            labels: xLabels,
            datasets: [{
                label: 'Ping',
                backgroundColor: color(window.chartColors.red).alpha(0.2).rgbString(),
                borderColor: window.chartColors.red,
                pointBackgroundColor: window.chartColors.red,
                data: igorPing,
            }, {
                label: 'Fed',
                backgroundColor: color(window.chartColors.green).alpha(0.2).rgbString(),
                borderColor: window.chartColors.green,
                pointBackgroundColor: window.chartColors.green,
                data: igorFed,
            }]
        };

        window.onload = function() {
            var chartEl = document.getElementById('chart1');
            new Chart(chartEl, {
                type: 'bar',
                data: lineChartData, 
                options: {
                    title: {
                        display: false,
                        text: ''
                    },
                }, 
            });
        };
    </script>
    </body>
</html>