.PHONY: protobuf test coverage

protobuf:
	protoc -I=protobuf --python_out=protobuf protobuf/status.proto
	protoc -I=protobuf --js_out=protobuf protobuf/status.proto

test:
	$(MAKE) -C server test
	$(MAKE) -C client/python test

coverage:
	$(MAKE) -C server coverage

clean:
	rm -rf server/.pytest_cache
	rm -rf server/gaia_server/__pycache
	rm -rf server/tests/__pycache
	rm -rf client/python/.pytest_cache
	rm -rf client/python/gaia_server/__pycache
	rm -rf client/python/tests/__pycache