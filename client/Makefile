.PHONY: install install-gpio-boot install-crons uninstall-crons install-services run gaia-running services-running kill autosync manual-feed manual-water water-fill-pipes cron-erase

LOGFILE_DIR=/var/log/gaia/
LOGFILE_INET=$(LOGFILE_DIR)inet_check.log
LOGFILE_STREAM=$(LOGFILE_DIR)stream_check.log
LOGFILE_GAIA=$(LOGFILE_DIR)gaia_check.log

install:
	sudo apt-get -y install python3 python3-pip autossh i2c-tools apache2-utils
	$(MAKE) -C python install

install-gpio-boot:
	# bad idea ! used by LCD screen now. echo "gpio -g mode 2 out" > /etc/rc.local

install-crons:
	mkdir -p $(LOGFILE_DIR)
	echo "*/30 * * * * root /root/gaia/client/cron/check_inet_connection.sh | rotatelogs -n 5 "${LOGFILE_INET}" 1M" > /etc/cron.d/check_inet_connection
	echo "*/2 * * * * root /root/gaia/client/cron/check_stream.sh | rotatelogs -n 5 "${LOGFILE_STREAM}" 1M" > /etc/cron.d/check_stream
	echo "*/1 * * * * root /root/gaia/client/run.sh | rotatelogs -n 5 "${LOGFILE_GAIA}" 1M" > /etc/cron.d/check_gaia
	echo "@reboot root /root/gaia/client/run.sh | rotatelogs -n 5 "${LOGFILE_GAIA}" 1M" > /etc/cron.d/check_gaia_reboot

list-crons:
	ls -al /etc/cron.d/

uninstall-crons:
	rm -f /etc/cron.d/check_inet_connection
	rm -f /etc/cron.d/check_stream
	rm -f /etc/cron.d/check_gaia 
	rm -f /etc/cron.d/check_gaia_reboot

install-services:
	sudo cp services/* /lib/systemd/system/
	sudo sudo chmod 644 /lib/systemd/system/autossh-ssh-tunnel.service
	sudo sudo chmod 644 /lib/systemd/system/stream.service
	systemctl start autossh-ssh-tunnel.service
	systemctl enable autossh-ssh-tunnel.service
	systemctl start stream.service
	systemctl enable stream.service

list-services:
	systemctl status autossh-ssh-tunnel.service

import-protobuf:
	$(MAKE) -C python import-protobuf

run:
	./run.sh > logs/run.txt

gaia-running:
	#ps -ux | grep "[p]ython2 gaia_client.py"

kill:
	pkill python
	pkill python2
	pkill python3

autosync:
	contscp . root@192.168.0.10:/root/gaia/client 22

manual-feed:
	cd python && python3 -c "from gaia_client.gpio_control import *; g = GPIOControl(); g.do_feeding()"

manual-water:
	cd python && python3 -c "from gaia_client.gpio_control import *; g = GPIOControl(); g.do_watering()"

water-fill-pipes:
	cd python && python3 -c "from gaia_client.gpio_control import *; g = GPIOControl(); g.fill_watering_tubes()"

cron-erase:
	rm -rf sqlite.db

test: $(SQLITE_DB)
	pytest -v --ignore=python/tests/hardware_test.py

coverage:
	rm -f .coverage
	$(MAKE) clean
	coverage run -m py.test -v --ignore=python/tests/hardware_test.py
