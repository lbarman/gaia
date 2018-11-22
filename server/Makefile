.PHONY: import-protobuf serve test freeze install coverage

PYTHON_MODULES=requirements.txt

import-protobuf:
	$(MAKE) -C ../protobuf all
	cp ../protobuf/protobufs_pb2.py gaia_server/
	cp ../protobuf/protobufs_pb2_grpc.py gaia_server/
	sed -i 's/import protobufs_pb2/import gaia_server.protobufs_pb2/g' gaia_server/protobufs_pb2_grpc.py

gaia_server/protobufs_pb2.py: import-protobuf
gaia_server/protobufs_pb2_grpc.py: import-protobuf

serve-grpc: gaia_server/protobufs_pb2.py gaia_server/protobufs_pb2_grpc.py
	python3 gaia_server/server_grpc.py

db.sqlite:
	python3 -c "import sys; sys.path.insert(0, 'gaia_server'); from database import *; Database().recreate_database()"

serve-web: db.sqlite
	gunicorn -w 4 -b 127.0.0.1:$(shell cat gaia_server/constants.py | grep WEB_SERVER_PORT | cut -d "=" -f 2 | xargs) --pythonpath gaia_server server_web:webserver

test: gaia_server/protobufs_pb2.py gaia_server/protobufs_pb2_grpc.py
	python3 tests/database_test.py
	python3 tests/server_grpc_test.py
	$(MAKE) -C . db.sqlite # the web server does *not* recreate the DB (since it is automatically spawned by gunicorn), so manually do it here
	python3 tests/server_web_test.py

freeze:
	pip freeze > $(PYTHON_MODULES)

install: $(PYTHON_MODULES)
	pip install -r $(PYTHON_MODULES)