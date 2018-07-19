.PHONY: install-cron install run autosync manual-feed

install:
	chmod u+x run.sh
	chmod u+x gaia-client.py

install-cron:
	echo "* * * * * root /root/gaia/client/run.sh" > /etc/cron.d/gaia 

run:
	./run.sh > logs/run.txt

is-running:
	ps -ux | grep "[p]ython2 gaia_client.py"

autosync:
	contscp . root@192.168.0.10:/root/gaia/client 22

manual-feed:
	python2 -c "from gpio_control import *; g=GPIOControl(); g.servoFeed()"