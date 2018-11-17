.PHONY: install clean cleanall test

PROTO_FILE=protobufs.proto
PYTHON_TARGET=protobufs_pb2.py
TEST_TARGET=protobuf_message_binary

$(PYTHON_TARGET): $(PROTO_FILE)
	# requires `pip install grpcio-tools --user`
	python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. protobufs.proto

all: clean $(PYTHON_TARGET)

clean:
	rm -f $(PYTHON_TARGET)
	rm -f $(TEST_TARGET)
	rm -rf __pycache__

test:
	python3 test.py $(TEST_TARGET)