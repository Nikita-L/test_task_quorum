# Test task Quorum  

## Installation  

1. Install Docker, Docker-compose  
2. Clone the repo: `git clone https://github.com/Nikita-L/test_task_quorum.git`  
3. `cd test_task_quorum`  
4. Build raft-consensus network: `make setup`  
5. Create contract `curl http://0.0.0.0:8000/create_contract`
6. To shutdown run: `make down`  

## Usage examples  

- update key value: `http://0.0.0.0:8000/update?key=somekey&value=somevalue`  
- get value: `http://0.0.0.0:8000/get?key=somekey`  
- remove key value: `http://0.0.0.0:8000/remove?key=somekey`  
- dump all data: `http://0.0.0.0:8000/dump?file=filename`  
