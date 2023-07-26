CHANGED_FILES = git diff --name-only --diff-filter=d | grep -E "\.py$" | tr "\n" " "
LOCAL_COMPOSE = docker compose run web
PIP_BIN =  $(LOCAL_COMPOSE) python -m pip
MANAGE_PY =  $(LOCAL_COMPOSE) python manage.py
ARG1 := $(word 2, $(MAKECMDGOALS) )
ARG2 := $(word 3, $(MAKECMDGOALS) )
ARG3 := $(word 4, $(MAKECMDGOALS) )

githook:
	@ git config --local core.hooksPath .githooks/

update:
	@ $(PIP_BIN) install -r requirements/local.txt

createsuperuser:
	@ $(MANAGE_PY) createsuperuser

shell:
	@ $(MANAGE_PY) shell

startapp:
	@ [ -z "$ARG2" ] && $(MANAGE_PY) startapp $(ARG1) --appdir $(ARG2) || $(MANAGE_PY) startapp $(ARG1)


startapi:
	@ [ -z "$ARG2" ] && $(MANAGE_PY) startapi $(ARG1) --appdir $(ARG2) || $(MANAGE_PY) startapi $(ARG1)


checkdb:
	@ [ -z "$ARG1" ] && $(MANAGE_PY) checkdb $(ARG1) || $(MANAGE_PY) checkdb

run-dev:
	python manage.py runserver 0.0.0.0:8000

run:
	python manage.py runserver 0.0.0.0:8000

pip:
	pip install -r ./requirements/production.txt

pip-dev:
	pip install -r ./requirements/local.txt

test:
	python manage.py test

up:
	docker compose -f ./docker-compose.local.yml up -d --build

down:
	docker compose -f ./docker-compose.local.yml down

format:
	black **/*.py --exclude '\.venv/|\.git/'

format-check:
	black **/*.py --check --exclude '\.venv/|\.git/'

lint:
	pylint --recursive=y .

lint-changed-files:
	FILES=$("$CHANGED_FILES") && [[ ! -z "$(FILES)" ]] && pylint --recursive=y "$(FILES)" || echo ""

qa-check:
	FILES=$("$CHANGED_FILES") && [[ ! -z "$(FILES)" ]] && pylint --recursive=y "$(FILES)" || echo ""
	black **/*.py --check --exclude '\.venv/|\.git/'

%:
	@:
