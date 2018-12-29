import socket
import gaia_server.constants as constants


def is_port_open(port):
    s = socket.socket()
    try:
        s.connect(('127.0.0.1', port))
        return True
    except socket.error:
        return False
    finally:
        s.close()


def build_port_open_html_string(is_open):

    css_class = 'portClosed'
    text = "?"

    if is_open:
        css_class = 'portOpen'
        text = "OK"

    return '<span class="portStatus ' + css_class + '">' + text + '</span>'


def build_water_levels_dict(l1, l2, l3, l4, dict):

    dict['WATER1_NUMBER'] = '?'
    dict['WATER2_NUMBER'] = '?'
    dict['WATER3_NUMBER'] = '?'
    dict['WATER4_NUMBER'] = '?'

    dict['WATER1_LEVEL'] = str(10)
    dict['WATER2_LEVEL'] = str(10)
    dict['WATER3_LEVEL'] = str(10)
    dict['WATER4_LEVEL'] = str(10)

    if l1 is not None:
        dict['WATER1_NUMBER'] = str(l1)
        dict['WATER1_LEVEL'] = str(round(l1 / constants.WATER_DURATION_EQUAL_100_PERCENT * 100))

    if l2 is not None:
        dict['WATER2_NUMBER'] = str(l2)
        dict['WATER2_LEVEL'] = str(round(l2 / constants.WATER_DURATION_EQUAL_100_PERCENT * 100))

    if l3 is not None:
        dict['WATER3_NUMBER'] = str(l3)
        dict['WATER3_LEVEL'] = str(round(l3 / constants.WATER_DURATION_EQUAL_100_PERCENT * 100))

    if l4 is not None:
        dict['WATER4_NUMBER'] = str(l4)
        dict['WATER4_LEVEL'] = str(round(l4 / constants.WATER_DURATION_EQUAL_100_PERCENT * 100))


def build_status_data_html(status):
    res = ''

    report_id = 0
    for s in status:

        feeding = '<span class="feedingColor">Feeding</span>: '
        if s['watering_module_activated'] == 0:
            feeding += '<span class="no">No</span>'
        else:
            feeding += '<span class="yes">Yes</span>'
        feeding += ', '+s['feeding_module_cronstring']

        watering = '<span class="wateringColor">Watering</span>: '
        if s['watering_module_activated'] == 0:
            watering += '<span class="no">No</span>'
        else:
            watering += '<span class="yes">Yes</span>'
        watering += ', '+s['watering_module_cronstring']

        water_levels = "{0},{1},{2},{3}".format(s['watering_pump_1_duration'], s['watering_pump_2_duration'], s['watering_pump_3_duration'], s['watering_pump_4_duration'])

        display_config = 'block'
        if report_id != 0:
            display_config = 'none'

        res += '''<div class="data status">
        <div class="reportId">#{id}</div>
        <div class="timestamp">
            <div class="server_ts">S: {server_ts}</div>
            <div class="local_ts">L: {local_ts}</div>
        </div>
        <div class="temperatures">
            Sensors: {t1}°/{humidity}%/{t2}°/{t3}°
        </div>
        <div class="system_status">
            <div class="uptime">{uptime}</div>
            <div class="memory">{memory}</div>
            <div class="disk_usage">{disk_usage}</div>
            <div class="processes">{processes}</div>
        </div>
        <div class="config" style="display:{displayConfig}">
            <div class="feeding">{feeding}</div>
            <div class="watering">{watering} (Pumps {waterlevels})</div>
        </div>
        </div>'''.format(id=s['id'],
                         server_ts=s['server_timestamp'].strftime("%H:%M:%S %d/%m/%Y"),
                         local_ts=s['local_timestamp'].strftime("%H:%M:%S %d/%m/%Y"),
                         t1=s['temperature'],
                         humidity=s['humidity'],
                         t2=round(s['temperature2']),
                         t3=round(s['temperature3']),
                         uptime=s['uptime'],
                         memory=s['memory'],
                         disk_usage=s['disk_usage'],
                         processes=s['processes'],
                         feeding=feeding,
                         watering=watering,
                         waterlevels=water_levels,
                         displayConfig=display_config)
        report_id += 1

    return res


def build_reports_data_html(reports):
    res = ''

    report_id = 0
    for r in reports:

        action_type = 'Undefined'
        type = 'unknown'
        if r['action_type'] == 1:
            action_type = '<span class="feedingColor">Feeding</span>'
            type = 'feeding'
        else:
            action_type = '<span class="wateringColor">Watering</span>'
            type = 'watering'

        res += '''<div class="data report {type}">
        <div class="reportId">#{id}</div>
        <div class="timestamp">
            <div class="server_ts">S: {server_ts}</div>
            <div class="local_ts">L: {local_ts}</div>
        </div>
        <div class="action_report">
            <div class="type">{action_type}</div>
            <div class="text">{details}</div>
        </div>
        </div>'''.format(id=r['id'],
                         server_ts=r['server_timestamp'].strftime("%H:%M:%S %d/%m/%Y"),
                         local_ts=r['local_timestamp'].strftime("%H:%M:%S %d/%m/%Y"),
                         action_type=action_type,
                         details=r['action_details'],
                         type=type)
        report_id += 1

    return res


def split_regex(regex):

    time = regex[0:regex.find('h')]
    days = regex[regex.find('h') + 2].strip()
    days_exploded = days.split(',')

    if days_exploded[0] == '*':
        days_exploded = [0,1,2,3,4,5,6]
    days_exploded = [int(x) for x in days_exploded]

    return [time, days_exploded]

def build_current_config(config):

    feeding_enabled = (config['feeding_module_activated'] == 1)
    watering_enabled = (config['watering_module_activated'] == 1)

    feeding_disabled = 'disabled'
    if feeding_enabled:
        feeding_disabled = ''

    water1level = 0
    water2level = 0
    water3level = 0
    water4level = 0
    water1number = ''
    water2number = ''
    water3number = ''
    water4number = ''

    watering_disabled = 'disabled'
    if watering_enabled:
        watering_disabled = ''
        water1level = max(100, round(100 * config['watering_pump_1_duration'] / constants.WATER_DURATION_EQUAL_100_PERCENT))
        water2level = max(100, round(100 * config['watering_pump_2_duration'] / constants.WATER_DURATION_EQUAL_100_PERCENT))
        water3level = max(100, round(100 * config['watering_pump_3_duration'] / constants.WATER_DURATION_EQUAL_100_PERCENT))
        water4level = max(100, round(100 * config['watering_pump_4_duration'] / constants.WATER_DURATION_EQUAL_100_PERCENT))
        water1number = config['watering_pump_1_duration']
        water2number = config['watering_pump_2_duration']
        water3number = config['watering_pump_3_duration']
        water4number = config['watering_pump_4_duration']

    feeding_splitted = split_regex(config['feeding_module_cronstring'])
    watering_splitted = split_regex(config['watering_module_cronstring'])
    feeding_time = feeding_splitted[0]
    watering_time = watering_splitted[0]

    [f0, f1, f2, f3, f4, f5, f6] = ['weekday_on' if feeding_enabled and day in feeding_splitted[1] else '' for day in range(0, 7)]
    [w0, w1, w2, w3, w4, w5, w6] = ['weekday_on' if watering_enabled and day in watering_splitted[1] else ''  for day in range(0, 7)]

    res = '''<div id="current_config">
            <h3>Current Config</h3>
            <div id="feeder-module" class="module {feeding_disabled}">
                <div class="foodbox">
                    <div class="foodpill" style="top:20px; left: 10px"></div>
                    <div class="foodpill" style="top:40px; left: 0px"></div>
                    <div class="foodpill" style="top:40px; left: 15px"></div>
                </div>
                <div class="label">Feeder</div>
            </div>

            <div id="water-module" class="module {watering_disabled}">
                <div id="glasscontainer">
                    <div id="glass1" class="glass"><div class="water" style="height:{water1level}%"></div><span>{water1number}</span></div>
                    <div id="glass2" class="glass"><div class="water" style="height:{water2level}%"></div><span>{water2number}</span></div>
                    <div id="glass3" class="glass"><div class="water" style="height:{water3level}%"></div><span>{water3number}</span></div>
                    <div id="glass4" class="glass"><div class="water" style="height:{water4level}%"></div><span>{water4number}</span></div>
                </div>
                <div class="label">Watering system</div>
            </div>

            <div id="weekdays-module" class="module">
                <div id="weekdays-feeder" class="weekdays {feeding_disabled}">
                    <table>
                        <tr>
                            <td class="{f0}">M</td>
                            <td class="{f1}">T</td>
                            <td class="{f2}">W</td>
                            <td class="{f3}">T</td>
                            <td class="{f4}">F</td>
                            <td class="{f5}">S</td>
                            <td class="{f6}">S</td>
                        </tr>
                    </table>
                    <span>@</span>
                    <div class="hour">{feeding_time}h</div>
                </div>
                <div id="weekdays-water" class="weekdays {watering_disabled}">
                    <table>
                        <tr>
                            <td class="{w0}">M</td>
                            <td class="{w1}">T</td>
                            <td class="{w2}">W</td>
                            <td class="{w3}">T</td>
                            <td class="{w4}">F</td>
                            <td class="{w5}">S</td>
                            <td class="{w6}">S</td>
                        </tr>
                    </table>
                    <span>@</span>
                    <div class="hour">{watering_time}h</div>
                </div>
            </div>
        </div>'''.format(feeding_disabled=feeding_disabled,
                         watering_disabled=watering_disabled,
                         water1level=water1level,
                         water2level=water2level,
                         water3level=water3level,
                         water4level=water4level,
                         water1number=water1number,
                         water2number=water2number,
                         water3number=water3number,
                         water4number=water4number,
                         feeding_time=feeding_time,
                         watering_time=watering_time,
                         f0=f0,
                         f1=f1,
                         f2=f2,
                         f3=f3,
                         f4=f4,
                         f5=f5,
                         f6=f6,
                         w0=w0,
                         w1=w1,
                         w2=w2,
                         w3=w3,
                         w4=w4,
                         w5=w5,
                         w6=w6)
    return res