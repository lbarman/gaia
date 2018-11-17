.PHONY: install clean cleanall test

PROTO_FILE=protobufs.proto

PYTHON_TARGET=protobufs_pb2.py
JS_TARGET=protobufs_pb2.js
TS_TARGET=protobufs_pb2.ts

node_modules/.installed:
	npm install
	touch node_modules/.installed

install: node_modules/.installed

$(PYTHON_TARGET): $(PROTO_FILE)
	protoc -I=. --python_out=. $(PROTO_FILE)
	protoc -I=. --go_out=. $(PROTO_FILE)

$(JS_TARGET): $(PROTO_FILE) install 
	./node_modules/protobufjs/bin/pbjs $(PROTO_FILE) -w commonjs -t static-module > $(JS_TARGET)

$(TS_TARGET): $(JS_TARGET) 
	./node_modules/protobufjs/bin/pbts $(JS_TARGET) > $(TS_TARGET)

all: clean $(PYTHON_TARGET) $(JS_TARGET) $(TS_TARGET)

clean:
	rm -f $(PYTHON_TARGET)
	rm -f $(JS_TARGET)
	rm -f $(TS_TARGET)
	rm -f test/out_python

cleanall:
	rm -rf node_modules
	rm -rf __pycache__

test:
	python3 test/write.py test/out_python