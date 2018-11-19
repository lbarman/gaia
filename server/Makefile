.PHONY: import-protobuf serve test freeze install

PYTHON_MODULES=requirements.txt

import-protobuf:
	$(MAKE) -C ../protobuf all
	cp ../protobuf/protobufs_pb2.py .
	cp ../protobuf/protobufs_pb2_grpc.py .

protobufs_pb2.py: import-protobuf
protobufs_pb2_grpc.py: import-protobuf

serve: protobufs_pb2.py protobufs_pb2_grpc.py
	python3 server-grpc.py

test: protobufs_pb2.py protobufs_pb2_grpc.py
	python3 database_test.py
	python3 server_grpc_test.py

$(PYTHON_MODULES):
	pip freeze > $(PYTHON_MODULES)

freeze: $(PYTHON_MODULES)

install: $(PYTHON_MODULES)
	pip install -r $(PYTHON_MODULES)