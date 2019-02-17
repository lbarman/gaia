import gaia_client.constants as constants
import gaia_client.cron as cron
import gaia_client.system as system
import gaia_client.grpc_client as grpc_client
import gaia_client.database as database
from datetime import datetime
import time

class GaiaClient:

    db = None
    system = None
    gpio = None
    grpc_client = None
    feeding_cron = None
    watering_cron = None

    def __init__(self):
        print("[GaiaClient] starting...")

        self.db = database.Database(in_memory=True)
        self.db.recreate_database()
        self.system = system.System()
        self.grpc_client = grpc_client.GRPC_Client(remote=constants.GAIA_GRPC_URL,
                                                   use_ssl=constants.GAIA_GRPC_USE_SSL,
                                                   db=self.grpc_client,
                                                   system=self.system)
        self.feeding_cron = cron.FeedingCron(db=self.db)
        self.watering_cron = cron.WateringCron(db=self.db)

        print("[GaiaClient] instantiated, db/system/grpc/cron OK")

    def run(self):
        sleep_count = 0

        while True:

            # toggle Logic LEDS on hardware
            self.gpio.toggle_feeding_led()
            self.gpio.toggle_watering_led()

            now = datetime.datetime.now()

            print("It is now", now)
            print("Feeding cron:", str(self.feeding_cron), "last run", self.feeding_cron.last_time_run(), "running in", (self.feeding_cron.next_occurrence(now) - now))
            print("Watering cron:", str(self.watering_cron), "last run", self.watering_cron.last_time_run(), "running in", (self.watering_cron.next_occurrence(now) - now))

            if self.feeding_cron.should_it_run(now):
                self.__feed()
            elif self.watering_cron.should_it_run(now):
                self.__water()
            elif sleep_count >= constants.GAIA_REPORT_EVERY_X_SLEEP:
                sleep_count = 0

                print
                "contacting Gaia now"
                answer = contactGaiaWebSite(now, getDataToUpload(now))

                if answer == "REBOOT" or answer == "RESTART":
                    contactGaiaWebSite(now, "Gaia requested reboot.")
                    system.reboot()
                if answer == "SHUTDOWN":
                    contactGaiaWebSite(now, "Gaia requested shutdown.")
                    system.shutdown()
                if answer == "FEED":
                    contactGaiaWebSite(now, "Gaia requested manual feeding.")
                    feed(now)
                if answer == "WATER":
                    contactGaiaWebSite(now, "Gaia requested manual plant watering.")
                    water(now)

            time.sleep(constants.WAITING_LOOP_SLEEP)
            sleep_count += 1

    def __feed(self):
        report = self.gpio.do_feeding()
        action_report = self.grpc_client.build_action_report_message(action="FEEDING", action_details=report)
        self.grpc_client.send_action_report_message(action_report=action_report)

    def __water(self):
        report = self.gpio.do_watering()
        action_report = self.grpc_client.build_action_report_message(action="WATERING", action_details=report)
        self.grpc_client.send_action_report_message(action_report=action_report)

