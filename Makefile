raft-network:
	cd test_task
	docker build -t quorum .
	cd Nnodes
	bash ./setup.sh
	docker-compose up -d
	cd ../..

deploy-contract:
	cd truffle_suite
	truffle migrate