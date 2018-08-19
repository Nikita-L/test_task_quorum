raft-network:
	cd test_task; docker build -t quorum .; cd Nnodes; bash ./setup.sh; docker-compose up -d
	docker ps -s

python-client:
	cd python_client; docker-compose up -d; docker-compose restart client
	docker ps -s

python-client-rebuild:
	cd python_client; docker-compose up --build -d
	docker ps -s

python-client-log:
	cd python_client; docker-compose logs -f client

python-client-down:
	cd python_client; docker-compose down
	docker ps -s

down:
	cd test_task/Nnodes; docker-compose down; bash ./cleanup.sh
	cd python_client; docker-compose down

containers-statistics:
	docker ps -s