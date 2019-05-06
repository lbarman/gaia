import gaia_client.constants as constants
import gaia_client.cron_with_default as cron
import gaia_client.system as system
import gaia_client.grpc_client as grpc_client
import gaia_client.database as database
from datetime import datetime
import time
import sys

db = database.Database(in_memory=False)
db.recreate_database()

def dummy():
    pass

action_handler = grpc_client.ActionHandler(shutdown_fn=dummy,
                                                   reboot_fn=dummy,
                                                   feed_fn=dummy,
                                                   water_fn=dummy,
                                                   reset_db_fn=dummy,
                                                   )

grpc_client = grpc_client.GRPC_Client(remote=constants.GAIA_GRPC_URL,
                                                   use_ssl=constants.GAIA_GRPC_USE_SSL,
                                                   db=db,
                                                   action_handler=action_handler)
temperature_sensors = {}
temperature_sensors['t1'] = 9
temperature_sensors['humidity'] = 9
temperature_sensors['t2'] = 9
temperature_sensors['t3'] = 9

m = grpc_client.build_status_message(temperature_sensors=temperature_sensors, system_status=None)
print("contacting Gaia now with", m)
answer = grpc_client.send_status_message(status_message=m)
print(answer)

action_report = grpc_client.build_action_report_message(action="FEEDING", action_details="some report")
print("Gonna send", action_report)
answer = grpc_client.send_action_report_message(action_report=action_report)
print(answer)
