black:
	black . --line-length 120

dbs:
	docker compose up redis elastic -d

tests_dev_up:
	docker compose -f tests/functional/docker-compose.yml up -d

tests_dev_down:
	docker compose -f tests/functional/docker-compose.yml down