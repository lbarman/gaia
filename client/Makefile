.PHONY: install-cron install run autosync manual-feed is-running kill manual-water

install:
	chmod u+x run.sh

install-cron:
	echo "* * * * * root /root/gaia/client/run.sh > /root/gaia/client/logs/cron.txt" > /etc/cron.d/gaia 

run:
	./run.sh > logs/run.txt

is-running:
	ps -ux | grep "[p]ython2 gaia_client.py"

autosync:
	contscp . root@192.168.0.10:/root/gaia/client 22

manual-feed:
	python2 -c "from gpio_control import *; g=GPIOControl(); g.servoFeed()"

manual-water:
	python2 -c "from gpio_control import *; g=GPIOControl(); g.waterPlants()"

print-cron-db:
	python2 -c "from cron import *; x=Cron(\"tmp\", \"0 *\"); x.debug_printDB()"

cron-erase-db:
	rm -rf sqlite.db

kill:
	pkill python
	pkill python2