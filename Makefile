mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(patsubst %/,%,$(dir $(mkfile_path)))

compose.test = -f docker-compose-test.yml
compose.prod = -f docker-compose-prod.yml

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

app_name=boilerplate-flask-api

all: run

build:
	docker compose build server
	@docker build -t $(app_name) .

run:
	docker compose up -d

logs:
	docker compose logs -f server

prod:
	docker compose -f docker-compose-prod.yml up -d

test:
	docker compose ${compose.test} run --rm server coverage run -m pytest $(filter-out $@,$(MAKECMDGOALS))

coverage:
	docker compose -f docker-compose-test.yml run --rm server coverage report

coverage_html:
	- docker compose -f docker-compose-test.yml run --rm server coverage html
	@echo "\033[0;32mHTML Report: \033[0;34m${current_dir}/app/coverage/html_coverage/index.html\033[0m"

lint:
	flake8

db:
	docker compose exec db psql -U postgres -d boilerplate

db_history:
	docker compose run --rm server flask db history

db_upgrade:
	docker compose exec -T server flask db upgrade

db_downgrade:
	docker compose run --rm server flask db downgrade

db_migrate:
ifndef MESSAGE
	$(error MESSAGE is not defined. Use make db_migrate MESSAGE="Create customers table")
else ifeq ($(strip $(MESSAGE)),)
	$(error MESSAGE cannot be empty. Use make db_migrate MESSAGE="Create customers table")
else
	docker compose exec -T server flask db migrate --message="$(MESSAGE)"
endif

shell:
	docker compose exec server flask shell

stop:
	docker compose down
