.PHONY: import-protobuf

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