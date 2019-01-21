.PHONY: install install-gpio-boot install-cron uninstall-cron install-services run gaia-running services-running kill autosync manual-feed manual-water water-fill-pipes cron-erase

install:
	sudo apt-get -y install python3-rpi.gpio autossh motion

install-gpio-boot:
	echo "gpio -g mode 2 out" > /etc/rc.local

install-cron:
	echo "* * * * * root /root/gaia/client/run.sh > /root/gaia/client/logs/cron.txt" > /etc/cron.d/gaia 

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
	python2 -c "from gpio_control import *; g=GPIOControl(); g.servoFeed()"

manual-water:
	python2 -c "from gpio_control import *; g=GPIOControl(); g.waterPlants()"

water-fill-pipes:
	python2 -c "from gpio_control import *; g=GPIOControl(); g.fillWaterPipes()"

cron-erase:
	rm -rf sqlite.db

uninstall-cron:
	rm -f /etc/cron.d/gaia 