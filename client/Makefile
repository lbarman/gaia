.PHONY: install install-gpio-boot install-cron uninstall-cron install-services run gaia-running services-running kill autosync manual-feed manual-water water-fill-pipes cron-erase

install:
	sudo apt-get -y install python3 python3-pip autossh motion i2c-tools
	$(MAKE) -C python install

install-gpio-boot:
	# bad idea ! used by LCD screen now. echo "gpio -g mode 2 out" > /etc/rc.local

install-cron:
	echo "* * * * * root /root/gaia/client/run.sh > /root/gaia/client/var/cron.gaia.log" > /etc/cron.d/gaia
	echo "*/30 * * * * /root/gaia/client/cron/check_inet_connection.sh > /root/gaia/client/var/cron.inet_test.log" > /etc/cron.d/inet_test

uninstall-cron:
	rm -f /etc/cron.d/gaia 

install-services:
	sudo cp services/* /lib/systemd/system/
	sudo sudo chmod 644 /lib/systemd/system/autossh-ssh-tunnel.service
	sudo sudo chmod 644 /lib/systemd/system/autossh-motion-tunnel.service
	systemctl start autossh-ssh-tunnel.service
	systemctl start autossh-motion-tunnel.service
	systemctl start motion
	systemctl enable autossh-ssh-tunnel.service
	systemctl enable autossh-motion-tunnel.service
	systemctl enable motion

import-protobuf:
	$(MAKE) -C python import-protobuf

run:
	./run.sh > logs/run.txt

gaia-running:
	ps -ux | grep "[p]ython2 gaia_client.py"

services-running:
	systemctl status autossh-ssh-tunnel.service
	systemctl status autossh-motion-tunnel.service
	systemctl status motion

kill:
	pkill python
	pkill python2

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
	pytest -v

coverage:
	rm -f .coverage
	$(MAKE) clean
	coverage run -m py.test -v
