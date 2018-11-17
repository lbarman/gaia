.PHONY: install run install-cron uninstall-cron get-external-ip run test is-running kill autosync manual-feed manual-water water-fill-pipes cron-print cron-erase

install:
	pip install google --user
	pip install google-cloud --user
	pip install google-cloud-vision --user

run:
	chmod u+x run.sh

install-gpio-boot:
	echo "gpio -g mode 2 out" > /etc/rc.local

install-cron:
	echo "* * * * * root /root/gaia/client/run.sh > /root/gaia/client/logs/cron.txt" > /etc/cron.d/gaia 

uninstall-cron:
	rm -f /etc/cron.d/gaia 

get-external-ip:
	curl icanhazip.com

run:
	./run.sh > logs/run.txt

test:
	python2 cron_test.py

is-running:
	ps -ux | grep "[p]ython2 gaia_client.py"

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

cron-print:
	python2 -c "from cron import *; x=Cron(\"tmp\", \"0 *\"); x.debug_printDB()"

cron-erase:
	rm -rf sqlite.db