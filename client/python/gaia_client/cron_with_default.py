import gaia_client.database as database
import gaia_client.constants as constants
import gaia_client.cron as cron

# CronWithDefault tries to load the config from the DB, or defaults to the given cronstring if something fails
class CronWithDefault(cron.Cron):

    def __init__(self, cron_name, cron_string_default=None, db=None):

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

            value_in_db = "NaN"

            if cron_name == "feeding_cron":
                value_in_db = config["feeding_module_cronstring"]
            else:
                value_in_db = config["watering_module_cronstring"]

            super().__init__(cron_name=cron_name, cron_string=value_in_db, db=db)

        except Exception as e:
            print("exception occurred when creating cron \"" + cron_name + "\", " + str(e) + ", defaulting to " + cron_string_default)
            super().__init__(cron_name=cron_name, cron_string=cron_string_default, db=db)


class FeedingCron(CronWithDefault):
    def __init__(self, db=None):
        super().__init__(cron_name="feeding_cron", cron_string_default=constants.FEEDING_DEFAULT_CRONSTRING, db=db)

class WateringCron(CronWithDefault):
    def __init__(self, db=None):
        super().__init__(cron_name="watering_cron", cron_string_default=constants.WATERING_DEFAULT_CRONSTRING, db=db)