setup:
	cd test_task; docker build -t quorum .; bash ./setup.sh
	docker-compose up -d
	docker-compose restart python_client
	docker ps -s

python-client:
	docker-compose up -d python_client; docker-compose restart python_client
	docker ps -s

python-client-rebuild:
	docker-compose up --build -d python_client
	docker ps -s

python-client-log:
	docker-compose logs -f python_client

python-client-python:
	docker-compose exec python_client python

redis-cli:
	docker-compose exec redis redis-cli

down:
	docker-compose down
	cd test_task; bash ./cleanup.sh

containers-statistics:
	docker ps -s