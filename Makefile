.PHONY: up down rebuild logs shell
ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(ARGS):;@:)

up:
	docker-compose up -d

down:
	docker-compose down

rebuild:
	docker-compose down
	docker-compose up -d --build

logs:
	docker-compose logs -f "${ARGS}"

shell:
	docker-compose exec "${ARGS}" bash