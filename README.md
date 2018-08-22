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
- dump all data in csv: `http://0.0.0.0:8000/dump?file=filename`  

## Add node  

1. Run: `make add-node`. On execution you will see enode string and ask to enter raft id. Copy enode string  
2. Open new terminal, run: `make node_1-geth`. Type: `var e = "` and paste copied enode string, type `";`. Press *Enter*. Provide `raft.addPeer(e);` and press *Enter*. There you will see number that represent your raft id, copy it  
3. Open previous terminal and paste copied raft id  

To check that peer is added, run: `make node_1-geth`, type `admin.peers`, press *Enter*. If you will see 3 items in the list, one of which will have *remoteAddress: "172.13.0.5:__port__"*, that is the sign that peer is added.  

To understand the logic of raft consensus work, see scenarios when new nodes are added or some nodes removed, review interactive raft consensus description: [link](http://thesecretlivesofdata.com/raft/)