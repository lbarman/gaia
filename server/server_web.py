from flask import Flask, Response, send_from_directory
from constants import WEB_SERVER_PORT, TEMPLATE_FILE

webserver = Flask(__name__, static_url_path='')


@webserver.route('/public/<path:filename>')
def assets(filename):
    return send_from_directory('public', filename)


@webserver.route('/')
def main():

    template_source = ''
    with open(TEMPLATE_FILE, 'r') as file:
        template_source = file.read()

    return Response(template_source, 200)


def start_web_server():
    global webserver
    webserver.run(host='127.0.0.1', port=WEB_SERVER_PORT)


if __name__ == '__main__':
    try:
        start_web_server()  # blocking
    except KeyboardInterrupt:
        print("Quitting")
