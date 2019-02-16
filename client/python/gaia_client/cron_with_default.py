import gaia_client.database as database
import gaia_client.constants as constants
import gaia_client.cron as cron

# CronWithDefault tries to load the config from the DB, or defaults to the given cronstring if something fails
class CronWithDefault(cron.Cron):

    enabled = True

    def __init__(self, cron_name, cron_string_default=None, cron_enabled=True, db=None):

        if cron_name != "feeding_cron" and cron_name != "watering_cron" :
            raise ValueError("cron_name has to be \"feeding_cron\" or \"watering_cron\"")

        if cron_string_default is None or cron_string_default.strip() == "" :
            raise ValueError("cron's default string can't be None! then just use a Cron")

        try:

            if db is None:
                raise Exception('db is null')

            if not isinstance(db, database.Database):
                raise Exception('db isn\'t a Database')

            config = db.get_config()

            if config is None:
                raise Exception('no config in DB')

            enabled_in_db = True
            cronstring_in_db = "NaN"

            if cron_name == "feeding_cron":
                enabled_in_db = config["feeding_module_activated"]
                cronstring_in_db = config["feeding_module_cronstring"]
            else:
                enabled_in_db = config["watering_module_activated"]
                cronstring_in_db = config["watering_module_cronstring"]

            self.enabled = enabled_in_db
            super().__init__(cron_name=cron_name, cron_string=cronstring_in_db, db=db)

        except Exception as e:
            print("exception occurred when creating cron \"" + cron_name + "\", " + str(e) + ", defaulting to " + cron_string_default + " (enabled)")
            self.enabled = cron_enabled
            super().__init__(cron_name=cron_name, cron_string=cron_string_default, db=db)

    def __str__(self):
        enabled_str = " (enabled)"
        if not self.enabled:
            enabled_str = " (disabled)"
        return str(self.cron_name) + ": " + str(self.hour) + "h on " + ','.join([constants.DAYS_STRING[x] for x in self.days]) + enabled_str

    def should_it_run(self, now):
        if not self.enabled:
            return False
        return super().should_it_run(now)


class FeedingCron(CronWithDefault):
    def __init__(self, db=None):
        super().__init__(cron_name="feeding_cron",
                         cron_string_default=constants.FEEDING_DEFAULT_CRONSTRING,
                         cron_enabled=constants.FEEDING_DEFAULT_ENABLED,
                         db=db)

class WateringCron(CronWithDefault):
    def __init__(self, db=None):
        super().__init__(cron_name="watering_cron",
                         cron_string_default=constants.WATERING_DEFAULT_CRONSTRING,
                         cron_enabled=constants.WATERING_DEFAULT_ENABLED,
                         db=db)