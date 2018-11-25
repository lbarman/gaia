.PHONY: protobuf test coverage

protobuf:
	protoc -I=protobuf --python_out=protobuf protobuf/status.proto
	protoc -I=protobuf --js_out=protobuf protobuf/status.proto

test:
	$(MAKE) -C server test
	$(MAKE) -C client/python test

coverage:
	$(MAKE) -C server coverage