.PHONY: run copy

static=flask_rest_1/static
static_node=$(static)/node_modules

run: copy
	python runserver.py

copy: $(static_node)

$(static_node): node_modules
	cp -r node_modules $(static)/node_modules

node_modules:
	npm install

