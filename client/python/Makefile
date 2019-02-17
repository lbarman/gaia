.PHONY: install run install-cron uninstall-cron get-external-ip run test is-running kill autosync manual-feed manual-water water-fill-pipes cron-print cron-erase

PYTHON_MODULES=requirements.txt

import-protobuf:
	@echo "Protobufs files are made by the server, if they don't exist, switch pyenv to server, and do \"make all\" in \"protobufs/\"."
	-cp ../../protobuf/protobufs_pb2.py gaia_client/
	-cp ../../protobuf/protobufs_pb2_grpc.py gaia_client/
	-sed -i 's/import protobufs_pb2/import gaia_client.protobufs_pb2/g' gaia_client/protobufs_pb2_grpc.py

gaia_client/protobufs_pb2.py: import-protobuf
gaia_client/protobufs_pb2_grpc.py: import-protobuf

db.sqlite:
	python3 -c "from gaia_client.cron import *; Cron()"

test: gaia_client/protobufs_pb2.py gaia_client/protobufs_pb2_grpc.py
	pytest -v

coverage:
	rm -f .coverage
	$(MAKE) clean
	coverage run -m py.test -v

clean:
	rm -rf db.sqlite

freeze:
	pip freeze > $(PYTHON_MODULES)

install: $(PYTHON_MODULES)
	pip install -r $(PYTHON_MODULES)