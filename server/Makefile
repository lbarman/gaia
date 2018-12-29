.PHONY: import-protobuf serve test freeze install coverage dummy_status

SQLITE_DB="data/db.sqlite"

PYTHON_MODULES=requirements.txt

import-protobuf:
	$(MAKE) -C ../protobuf all
	cp ../protobuf/protobufs_pb2.py gaia_server/
	cp ../protobuf/protobufs_pb2_grpc.py gaia_server/
	sed -i 's/import protobufs_pb2/import gaia_server.protobufs_pb2/g' gaia_server/protobufs_pb2_grpc.py

gaia_server/protobufs_pb2.py: import-protobuf
gaia_server/protobufs_pb2_grpc.py: import-protobuf

serve-grpc:
	PYTHONPATH=$(shell pwd) python3 gaia_server/server_grpc.py

db: $(SQLITE_DB)

$(SQLITE_DB):
	python3 -c "from gaia_server.database import *; Database().recreate_database()"

serve-web: $(SQLITE_DB)
	gunicorn -w 4 -b 0.0.0.0:$(shell cat gaia_server/constants.py | grep WEB_SERVER_PORT | cut -d "=" -f 2 | xargs) --pythonpath gaia_server server_web:webserver

test: gaia_server/protobufs_pb2.py gaia_server/protobufs_pb2_grpc.py
	pytest -v

coverage:
	rm -f .coverage
	$(MAKE) clean
	coverage run -m py.test -v

clean:
	rm -rf $(SQLITE_DB)

freeze:
	pip freeze > $(PYTHON_MODULES)

install: $(PYTHON_MODULES)
	pip install -r $(PYTHON_MODULES)

dummy_status: $(SQLITE_DB)
	python3 -c "from tests.pings_dummy import *; insert_dummy_pings()"