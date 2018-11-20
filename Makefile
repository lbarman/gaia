.PHONY: protobuf install-server test

install-server:
	$(MAKE) -C server install

protobuf:
	protoc -I=protobuf --python_out=protobuf protobuf/status.proto
	protoc -I=protobuf --js_out=protobuf protobuf/status.proto	

test:
	$(MAKE) -C server test