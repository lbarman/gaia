import socket
from constants import WATER_DURATION_EQUAL_100_PERCENT


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
        dict['WATER1_LEVEL'] = str(round(l1 / WATER_DURATION_EQUAL_100_PERCENT * 100))

    if l2 is not None:
        dict['WATER2_NUMBER'] = str(l2)
        dict['WATER2_LEVEL'] = str(round(l2 / WATER_DURATION_EQUAL_100_PERCENT * 100))

    if l3 is not None:
        dict['WATER3_NUMBER'] = str(l3)
        dict['WATER3_LEVEL'] = str(round(l3 / WATER_DURATION_EQUAL_100_PERCENT * 100))

    if l4 is not None:
        dict['WATER4_NUMBER'] = str(l4)
        dict['WATER4_LEVEL'] = str(round(l4 / WATER_DURATION_EQUAL_100_PERCENT * 100))