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

        feeding = 'Feeding: '
        if s['watering_module_activated'] == 0:
            feeding += 'No'
        else:
            feeding += 'Yes'
        feeding += ', '+s['feeding_module_cronstring']

        watering = 'Watering: '
        if s['watering_module_activated'] == 0:
            watering += 'No'
        else:
            watering += 'Yes'
        watering += ', '+s['watering_module_cronstring']

        water_levels = "{0},{1},{2},{3}".format(s['watering_pump_1_duration'], s['watering_pump_2_duration'], s['watering_pump_3_duration'], s['watering_pump_4_duration'])

        display_config = 'block'
        if report_id != 0:
            display_config = 'none'

        res += '''<div class="data">
        <div class="reportId">#{id}</div>
        <div class="timestamp">
            <div class="server_ts">S: {server_ts}</div>
            <div class="local_ts">L: {local_ts}</div>
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
        </div>'''.format(id=report_id,
                         server_ts=s['server_timestamp'].strftime("%H:%M:%S %d/%m/%Y"),
                         local_ts=s['local_timestamp'].strftime("%H:%M:%S %d/%m/%Y"),
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
