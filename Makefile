install:
	poetry install

test:
	poetry run python manage.py test

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8 task_manager

selfcheck:
	poetry check

check: selfcheck lint test

dev:
	poetry run python manage.py runserver

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
.PHONY: install

all: schema-load start

schema-load:
	psql railway < database.sql

generate:
	node ./bin/load.js

db-reset:
	dropdb railway || true
	createdb railway

db-create:
	createdb task_manager || echo 'skip'

connect:
	psql -d task_manager

shell:
	python manage.py shell_plus --ipython

test-coverage:
	poetry run coverage run manage.py test -v 2 && poetry run coverage xml
