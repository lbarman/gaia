.PHONY: import-protobuf serve test freeze install

PYTHON_MODULES=requirements.txt

import-protobuf:
	$(MAKE) -C ../protobuf all
	cp ../protobuf/protobufs_pb2.py .
	cp ../protobuf/protobufs_pb2_grpc.py .

protobufs_pb2.py: import-protobuf
protobufs_pb2_grpc.py: import-protobuf

serve-grpc: protobufs_pb2.py protobufs_pb2_grpc.py
	python3 server-grpc.py

db.sqlite:
	python3 -c "from database import *; Database().recreate_database()"

serve-web: db.sqlite
	gunicorn -w 4 -b 127.0.0.1:$(shell cat constants.py | grep WEB_SERVER_PORT | cut -d "=" -f 2 | xargs) server_web:webserver

test: protobufs_pb2.py protobufs_pb2_grpc.py
	python3 database_test.py
	python3 server_grpc_test.py

freeze:
	pip freeze > $(PYTHON_MODULES)

install: $(PYTHON_MODULES)
	pip install -r $(PYTHON_MODULES)
