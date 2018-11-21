.PHONY: protobuf install-server test

protobuf:
	protoc -I=protobuf --python_out=protobuf protobuf/status.proto
	protoc -I=protobuf --js_out=protobuf protobuf/status.proto

test:
	$(MAKE) -C . test

coverage:
	rm -f .coverage
	coverage run -a --source=server server/database_test.py
	coverage run -a --source=server server/server_grpc_test.py
	$(MAKE) -C server db.sqlite # the web server does *not* recreate the DB (since it is automatically spawned by gunicorn), so manually do it here
	coverage run -a --source=server server/server_web_test.py
	coveralls
