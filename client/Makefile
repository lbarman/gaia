.PHONY: install-cron

install:
	chmod u+x run.sh
	chmod u+x gaia-client.py

install-cron:
	echo "* * * * * root /root/gaia/client/run.sh" > /etc/cron.d/gaia 

run:
	./