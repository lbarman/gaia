from flask import Flask, Response, send_from_directory, request

import protobufs_pb2
from constants import *
from helpers import *
from database import Database
from time import sleep
import re
import os

webserver = Flask(__name__, static_url_path='')


@webserver.route('/public/<path:filename>')
def assets(filename):
    public_path = os.path.join(os.getcwd(), "public")
    return send_from_directory(public_path, filename)


@webserver.route('/command', methods=['POST'])
def update_command():
    try:
        # very weak protection against bruteforce
        sleep(WEB_SERVER_NEW_COMMAND_SLEEP_TIME)

        if request.form is None:
            return Response(status=400)
        if request.form.get('passphrase') != COMMAND_PASSPHRASE:
            return Response(status=401)

        cmd_id = request.form.get('newCommand')
        cmd_text = 'UNKNOWN_COMMAND'
        if cmd_id == '0':
            cmd_text = 'DO_NOTHING'
        elif cmd_id == '1':
            cmd_text = 'SHUTDOWN'
        elif cmd_id == '2':
            cmd_text = 'REBOOT'
        else:
            return Response(status=406)

        new_config = None

        if request.form.get('updateConfig') == '1':
            new_config = protobufs_pb2.Config()

            # manually parse those
            new_config.feeding_module_activated = False
            if request.form.get('feedingEnabled') == '1':
                new_config.feeding_module_activated = True

            new_config.watering_module_activated = False
            if request.form.get('wateringEnabled') == '1':
                new_config.watering_module_activated = True

            # regex-validate those
            feeding_cron = request.form.get('feedingCron')
            watering_cron = request.form.get('wateringCron')

            pattern = re.compile(CRON_REGEX_TESTER)
            if not pattern.match(feeding_cron):
                raise ValueError('Feeding cron is invalid:', feeding_cron)
            if not pattern.match(watering_cron):
                raise ValueError('Watering cron is invalid:', feeding_cron)

            new_config.feeding_module_cronstring = feeding_cron
            new_config.watering_module_cronstring = watering_cron

            # manual sanity check on those values
            d1 = int(request.form.get('pump1Duration'))
            d2 = int(request.form.get('pump2Duration'))
            d3 = int(request.form.get('pump3Duration'))
            d4 = int(request.form.get('pump4Duration'))

            if d1 < 0 or d2 < 0 or d3 < 0 or d4 < 0:
                raise ValueError('A watering duration is below zero:', d1, d2, d3, d4)

            m = WATERING_DURATION_MAX_VALUE
            if d1 > m or d2 > m or d3 > m or d4 > m:
                raise ValueError('A watering duration exceeds the max value:', d1, d2, d3, d4)

            # protobuf raise exception if we're not actually inputting numbers
            new_config.watering_pump_1_duration = d1
            new_config.watering_pump_2_duration = d2
            new_config.watering_pump_3_duration = d3
            new_config.watering_pump_4_duration = d4

        db = Database()
        db.save_command(cmd_text, new_config)
        return Response(status=201)

    except Exception as e:
        print("Exception: ", e)
        return Response(status=400)


@webserver.route('/')
def main():

    template_source = ''
    with open(TEMPLATE_FILE, 'r') as file:
        template_source = file.read()

    # query the database
    db = Database()
    next_command = db.get_command()
    all_status = db.get_all_status()

    next_cmd_string = '&bot;'
    if next_command is not None:
        next_cmd_string = next_command['text']

    all_status_string = ''
    for status in all_status:
        print(status)

    # prepare the array to replace in the template
    tokens = dict()
    tokens['TEST_PORT_SSH'] = build_port_open_html_string(is_port_open(PORT_SSH))
    tokens['TEST_PORT_VIDEO'] = build_port_open_html_string(is_port_open(PORT_VIDEO))
    tokens['DATA'] = 'On'
    tokens['NEXT_COMMAND'] = next_cmd_string
    tokens['PORT_VIDEO'] = str(PORT_VIDEO)
    build_water_levels_dict(None, None, 100, None, tokens)

    tokens['FEEDING_HOUR'] = '12'
    tokens['WATERING_HOUR'] = '14'

    tokens['FEEDING_DISABLED'] = ''  # 'disabled'
    tokens['WATERING_DISABLED'] = ''  # 'disabled'

    # build the template
    html = template_source
    for key in tokens:
        html = html.replace('{{' + key + '}}', tokens[key])

    return Response(html, 200)


# BTW: gunicorn is directly calling webserver.run itself. make sure the DB exists, it is not created by the web server
if __name__ == '__main__':
    try:
        webserver.run(host='127.0.0.1', port=WEB_SERVER_PORT)
    except KeyboardInterrupt:
        print("Quitting")
