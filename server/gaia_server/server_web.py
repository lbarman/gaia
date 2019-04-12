import time
import os
import re
from flask import Flask, Response, send_from_directory, request
import gaia_server.constants as constants
import gaia_server.database as database
import gaia_server.helpers as helpers
import gaia_server.protobufs_pb2 as protobufs_pb2

webserver = Flask(__name__, static_url_path='')


@webserver.route('/public/<path:filename>')
def assets(filename):
    public_path = os.path.join(os.getcwd(), "public")
    return send_from_directory(public_path, filename)


def save_new_config_to_db(cmd_text = 'UNKNOWN_COMMAND'):
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

        pattern = re.compile(constants.CRON_REGEX_TESTER)
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

        m = constants.WATERING_DURATION_MAX_VALUE
        if d1 > m or d2 > m or d3 > m or d4 > m:
            raise ValueError('A watering duration exceeds the max value:', d1, d2, d3, d4)

        # protobuf raise exception if we're not actually inputting numbers
        new_config.watering_pump_1_duration = d1
        new_config.watering_pump_2_duration = d2
        new_config.watering_pump_3_duration = d3
        new_config.watering_pump_4_duration = d4

    db = database.Database()
    db.save_command(cmd_text, new_config)

@webserver.route('/command', methods=['POST'])
def update_command():
    try:
        # very weak protection against bruteforce
        time.sleep(constants.WEB_SERVER_NEW_COMMAND_SLEEP_TIME)

        if request.form is None:
            return Response(status=400)
        if request.form.get('passphrase') != constants.COMMAND_PASSPHRASE:
            return Response(status=401)

        cmd_id = request.form.get('newCommand')
        if cmd_id == '0':
            save_new_config_to_db('DO_NOTHING')
        elif cmd_id == '1':
            save_new_config_to_db('SHUTDOWN')
        elif cmd_id == '2':
            save_new_config_to_db('REBOOT')
        elif cmd_id == '3': # empty server db
            db = database.Database()
            db.recreate_database()
            db.truncate()
        elif cmd_id == '4': # reset server db to dummy config
            db = database.Database()
            db.recreate_database()
            db.truncate()
            import tests.dummy_data as dummy_data
            dummy_data.insert_dummy_action_report()
            dummy_data.insert_dummy_pings()
        else:
            return Response(status=406)


        return Response(status=201)

    except Exception as e:
        print("Exception: ", e)
        return Response(status=400)


@webserver.route('/')
def main():

    template_source = ''
    template_file = os.path.join(os.getcwd(), "templates", constants.TEMPLATE_FILE)
    with open(template_file, 'r') as file:
        template_source = file.read()

    # query the database
    db = database.Database()
    next_command = db.get_command()
    all_status = db.get_all_status()
    all_reports = db.get_all_action_reports()

    next_cmd_string = '&bot;'
    if next_command is not None:
        next_cmd_string = next_command['text']

    # prepare the array to replace in the template
    tokens = dict()
    tokens['STATUS'] = helpers.build_status_data_html(all_status)
    tokens['REPORTS'] = helpers.build_reports_data_html(all_reports)
    if len(all_status) > 0:
        tokens['CURRENT_CONFIG'] = helpers.build_current_config(all_status[0])
    else:
        tokens['CURRENT_CONFIG'] = '<div id="current_config"><h3>Current Config</h3>No config</div>'
    tokens['JS_ARRAYS'] = helpers.build_js_arrays(all_status, all_reports)
    tokens['NEXT_COMMAND'] = next_cmd_string
    tokens['PORT_VIDEO'] = str(constants.PORT_VIDEO)
    helpers.build_water_levels_dict(None, None, 100, None, tokens)


    # build the template
    html = template_source
    for key in tokens:
        html = html.replace('{{' + key + '}}', tokens[key])

    return Response(html, 200)


# BTW: gunicorn is directly calling webserver.run itself. make sure the DB exists, it is not created by the web server
if __name__ == '__main__':
    try:
        webserver.run(host='127.0.0.1', port=constants.WEB_SERVER_PORT)
    except KeyboardInterrupt:
        print("Quitting")
