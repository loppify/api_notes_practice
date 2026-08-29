.PHONY: up down rebuild logs shell

up:
	docker-compose up -d

down:
	docker-compose down

rebuild:
	docker-compose down
	docker-compose up --rebuild -d

logs:
	docker-compose logs -f app

shell:
	docker-compose exec app bash