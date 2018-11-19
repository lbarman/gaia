from flask import Flask, Response, send_from_directory
from constants import *
from helpers import *
from database import Database

webserver = Flask(__name__, static_url_path='')


@webserver.route('/public/<path:filename>')
def assets(filename):
    return send_from_directory('public', filename)


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

    tokens['FEEDING_DISABLED'] = '' # 'disabled'
    tokens['WATERING_DISABLED'] = '' #'disabled'

    # build the template
    html = template_source
    for key in tokens:
        html = html.replace('{{' + key + '}}', tokens[key])

    return Response(html, 200)


# BTW: gunicorn is directly calling webserver.run itself
if __name__ == '__main__':
    try:
        webserver.run(host='127.0.0.1', port=WEB_SERVER_PORT)
    except KeyboardInterrupt:
        print("Quitting")
