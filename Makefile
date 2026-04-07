build:
	docker compose build

up:
# 	export HOST_AUTH_LOG_PATH=/var/log/auth.log
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=250