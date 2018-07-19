.PHONY: install-cron install run autosync

install:
	chmod u+x run.sh
	chmod u+x gaia-client.py

install-cron:
	echo "* * * * * root /root/gaia/client/run.sh" > /etc/cron.d/gaia 

run:
	./

autosync:
	contscp . root@192.168.0.10:/root/gaia/client 22