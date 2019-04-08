#!/bin/bash

if [ `ps ax | grep "[p]ython3 gaia_entrypoint.py" | wc -l` -ne 1 ]; then
    echo "Restarting gaia..."
    pkill python
    pkill python3
    cd /root/gaia/client/python && nohup python3 gaia_entrypoint.py >/tmp/gaia.log 2>&1 &
else
    echo "Process already running, all good."
fi