.PHONY: protobuf

protobuf:
	protoc -I=protobuf --python_out=protobuf protobuf/status.proto
	protoc -I=protobuf --js_out=protobuf protobuf/status.proto	