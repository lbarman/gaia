.PHONY: cleanall serve serve-dev install rebuild-views build
VIEWS=$(shell find src/view/ -type f -name '*.top.ts')

yarn.lock:
	yarn install

node_modules/built:
	yarn install
	touch node_modules/built

install: package.json yarn.lock
	$(MAKE) node_modules/built

cleanall:
	rm -rf node_modules
	rm -rf dist

# Used for production
build: install
	node_modules/typescript/bin/tsc
	cp -r src/public dist/src

serve: build
	cd dist && node src/index.js

dev: 
	npx npm-run-all --parallel watch-view watch-server watch-sass

# Used for local development
serve-dev: install
	npm start

build-server: install
	nodemon --config nodemon-server.json

build-view: install
	nodemon --config nodemon-views.json

build-sass: install
	nodemon --config nodemon-sass.json

# Automatic view rebuild with "make view-dev"
src/public/css/index.css: src/public/css/index.scss
	npx sass src/public/css/index.scss > src/public/css/index.css

rebuild-sass: src/public/css/index.css

# Automatic view rebuild with "make view-dev"
%.top.ts: %.top.html
	topside $<

rebuild-views: $(VIEWS)

# DB-related stuff
remove-db:
	rm -f database.sqlite

importFromCsvs: remove-db
	ts-node import.ts