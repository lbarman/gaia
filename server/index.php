<?php
require_once("db.php");
require_once("config.php");

$NUMBER_OF_ITEMS_TO_FETCH = 10000;

function formatTime($t){
    $seconds = strtotime($t);
    return date('H:i:s, d.m.Y', $seconds);
}

function startsWith($haystack, $needle)
{
     $length = strlen($needle);
     return (substr($haystack, 0, $length) === $needle);
}

function handleRaspberryConnection($db, $nextCommand){
    if(isset($_GET['ping'])) {
        $secretToken = CLIENT_TOKEN;
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

            // truncate the DB
            $oneWeekAgo = date("Y-m-d H:i:s", strtotime("-1 week"));
            $s = "DELETE FROM `pings` WHERE `timestamp`<'" . $oneWeekAgo ."';";
            $db->query($s);

            // empty commands
            $s = "DELETE FROM `commands` WHERE 1=1;";
            $db->query($s);

            die($nextCommand);
        }
        else
        {
            sleep(3);
            die('Invalid secret');
        }
    }
}

function testPort($port){

    $red='rgb(255, 99, 132)';
    $green='rgb(75, 192, 192)';

    if(@fsockopen('lbarman.ch', $port, $errno, $errstr, 2))
    {
        return '<span style="color:'.$green.';font-weight:bold;">OK</span>';
    }
    return '<span style="color:'.$red.';font-weight:bold;">?</span>';
}

$db = new Db();

// handle the eventual command creation
if(isset($_POST) && isset($_POST['passphrase']) && isset($_POST['newCommand'])){
    if($_POST['passphrase'] !== COMMAND_PASSPHRASE){
        sleep(3);
        die("Invalid passphrase");
    } else {
        $cmd = strtoupper(trim($_POST['newCommand']));
        $s = "INSERT INTO `commands` (`id`, `timestamp`, `command`) VALUES (NULL, CURRENT_TIMESTAMP, '" . $cmd ."');";
        $db->query($s);
    }
}

// fetch potential command
$nextCommand = "OK";
$commands = $db->select("SELECT id,timestamp,command FROM `commands` ORDER BY timestamp DESC LIMIT 1");
if(count($commands) > 0) {
    $nextCommand = $commands[0]["command"];
}

handleRaspberryConnection($db, $nextCommand); # check if connection is a ping from the Raspberry

?>

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Gaia</title>
        <link rel="stylesheet" type="text/css" href="sakura.css">
        <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.min.js"></script>
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

        .uninteresting_report {
            display: none;
        }
        iframe {
            width: 100%;
            height: 500px;
            background-color: black;
        }
        #logo {
            float: left;
            margin-right: 30px;
        }

        h1 {
            margin-top: 30px;
            margin-bottom: 40px;
        }
        body {
            background-color: white;
        }
    </style>
    </head>
    <body>
        <img id="logo" src="images/gaia.jpg" width="100" height="97" />
        <h1>Gaia</h1>
        <div>
            <p>Connectivity: Ping=<?php echo testPort(11734); ?> Video=<?php echo testPort(11735);?></p>
            <p><a href="#" onclick="loadFeed()">Load live feed</a></p>
            <div id="live_feed"></div>

            <h3>Graph</h3>
            <div id="canvas-holder1" style="width:100%;">
                <canvas id="chart1"></canvas>
            </div>

            <div>
                <?php

                    $rows = $db->select("SELECT id,timestamp,local_timestamp,data FROM `pings` ORDER BY timestamp DESC LIMIT ".$NUMBER_OF_ITEMS_TO_FETCH);
                    
                    $toInt = function($s) {
                        return (int)$s;
                    };

                    //for each xTick, check if we have something to print 
                    $igorPing = array();
                    $igorFed = array();
                    $plantsWatered = array();

                    foreach($rows as $row) {
                        $str = $row['local_timestamp'];
                        $ts = (int)strtotime($row['local_timestamp']);
                            
                        $data = base64_decode($row['data']);
                        if($data == "Feeded"){
                            $igorFed[$ts] = 1;
                        } else if(startsWith($data, "Starting plant watering")){
                            $plantsWatered[$ts] = 1;
                        } else {
                            $igorPing[$ts] = 1;
                        }
                    }

                    #$maxValue = max(array(max($igorPing), max($igorPing), max($igorPing)));
                    #$igorFed = array_map(function($el) { return $el * $maxValue; }, $igorFed);
                    #$plantsWatered = array_map(function($el) { return $el * $maxValue; }, $plantsWatered);

                    //print igorFed for js
                    echo '<script>var a1 = {};';
                    foreach($igorFed as $k => $v){

                        echo 'a1["'.$k.'"] = \''.$v.'\';';
                    }

                    //print igorPing for js
                    echo 'var a2 = {};'."\n";
                    foreach($igorPing as $k => $v){

                        echo 'a2["'.$k.'"] = \''.$v.'\';';
                    }

                    //print plantsWatered for js
                    echo 'var a3 = {};';
                    foreach($plantsWatered as $k => $v){

                        echo 'a3["'.$k.'"] = \''.$v.'\';';
                    }
                    echo "\n".'var igorFed = a1;'."\n";
                    echo 'var igorPing = a2;'."\n";
                    echo 'var plantsWatered = a3;'."\n";
                    echo '</script>';
                    ?>
                    <pre id="graphData">

                    </pre>
            </div>
        </div>
        <div>
            <h3>Commands</h3>
            <pre><?php echo ($nextCommand == "OK" ? '&bot;' : $nextCommand); ?></pre>
            <form method="post">
                <p>Add new command:</p>
                <input id="newCommand"  name="newCommand" placeholder="COMMAND" type="text" />
                <input id="passphrase"  name="passphrase" placeholder="Passphrase" type="password" />
                <input type="submit"></input>
            </form>
        </div>
        <div>
            <h3>Data</h3>
            <?php

                $hiddenReports = 0;
                $first = true;

                foreach($rows as $row) {

                    $data = base64_decode($row['data']);
                    $class = '';
                    if (!$first && startsWith($data, '# feed igor')){
                        $class = 'uninteresting_report';
                        $hiddenReports++;
                    }

                    echo '<div class="'.$class.'">';
                    echo '<h5>[#'.$row['id'].'] '.
                        formatTime($row['local_timestamp']).'</h5>';
                    echo 'Created at '.formatTime($row['timestamp']);

                    echo '<pre>'.base64_decode($row['data']).'</pre>';
                    echo '</div>';

                    $first = false;
                }
                echo '<p>'.$hiddenReports.' hidden reports (<a href="" onclick="$(\'.uninteresting_report\').css(\'display\', \'block\');">show</a>)</p>';
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

        var PRECISION = 24 * 3600

        function roundTo(x) {
            return Math.floor(x / PRECISION) * PRECISION
        }

        function toDataset(rawData, labels) {
            var hashMap = {}
            for (var property in rawData) {
                if (rawData.hasOwnProperty(property)) {

                    t = roundTo(Number(property))
                    if(hashMap[t] == undefined){
                       hashMap[t] = 0 
                    }
                    hashMap[t] += Number(rawData[property])
                }
            }
            if(labels == undefined){
                // we compute our own labels
                labels = []
                var dataset = []
                for (var property in hashMap) {
                    if (hashMap.hasOwnProperty(property)) {
                        t = new Date(1000 * Number(property))
                        labels.push(t)
                        dataset.push({t: t, y: hashMap[property]});
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
                        dataset.push({t: t, y: 1});
                    } else {
                        dataset.push({t: t, y: 0});
                    }
                }
                return [labels, dataset]
            }
        }

        var pingsLabelsAndVals = toDataset(igorPing, undefined);
        var igorLabelsAndVals = toDataset(igorFed, pingsLabelsAndVals[0]);
        var plantsLabelsAndVals = toDataset(plantsWatered, pingsLabelsAndVals[0]);

        // nice labels
        var labels = [];
        for (i = 0; i < pingsLabelsAndVals[0].length; i++) {
            d = pingsLabelsAndVals[0][i];
            labels.push(d.getDate()+"/"+(d.getMonth()+1) + " " + d.getHours());
        }

        // make the important info stand out
        maxValue = 0
        for (i = 0; i < pingsLabelsAndVals[1].length; i++) {
            maxValue = Math.max(maxValue, pingsLabelsAndVals[1][i].y)
        }
        maxValue = -maxValue
        for (i = 0; i < igorLabelsAndVals[1].length; i++) {
            igorLabelsAndVals[1][i].y = maxValue * igorLabelsAndVals[1][i].y
        }
        for (i = 0; i < plantsLabelsAndVals[1].length; i++) {
            plantsLabelsAndVals[1][i].y = maxValue * plantsLabelsAndVals[1][i].y
        }

        // print interesting info
        igorUnprocessedData = toDataset(igorFed, undefined);
        str = "# igor fed:" + "\n"
        for (var property in igorFed) {
            if (igorFed.hasOwnProperty(property)) {
                t = new Date(1000 * Number(property))
                str += t.toUTCString().replace(" GMT", "") + "\n"
            }
        }
        str += "\n"
        str += "# plants watered:" + "\n"
        for (var property in plantsWatered) {
            if (plantsWatered.hasOwnProperty(property)) {
                t = new Date(1000 * Number(property))
                str += t.toUTCString().replace(" GMT", "") + "\n"
            }
        }
        
        $('#graphData').html(str)

        // plot
        var red = 'rgb(255, 99, 132)'
        var green = 'rgb(75, 192, 192)'
        var blue = 'rgb(54, 162, 235)'

        var color = Chart.helpers.color;
        var lineChartData = {
            labels: labels,
            datasets: [{
                label: 'Ping',
                backgroundColor: color(blue).alpha(0.2).rgbString(),
                borderColor: blue,
                pointBackgroundColor: blue,
                data: pingsLabelsAndVals[1],
            }, {
                label: 'Igor Fed',
                backgroundColor: color(red).alpha(0.2).rgbString(),
                borderColor: red,
                pointBackgroundColor: red,
                data: igorLabelsAndVals[1],
            }, {
                label: 'Plants Watered',
                backgroundColor: color(green).alpha(0.2).rgbString(),
                borderColor: green,
                pointBackgroundColor: green,
                data: plantsLabelsAndVals[1],
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

        function loadFeed(){
            $('#live_feed').html('<iframe src="http://lbarman.ch:11734"></iframe>');
            return false;
        }
    </script>
    </body>
</html>