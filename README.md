# Test task Quorum  

## Installation  

1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads), [Vagrant](https://www.vagrantup.com/downloads.html), Truffle
2. Clone the repo: `git clone https://github.com/Nikita-L/test_task_quorum.git`  
3. `cd test_task_quorum`  
4. `vagrant up`
5. To shutdown run: `vagrant suspend`; delete vagrant instance: `vagrant destroy`  

## Setup Raft-based Consensus
1. `vagrant ssh`
2. `cd test_task`
3. `./raft-init.sh`
4. `./raft-start.sh`

# Deploy smart contract on Quorum
Open separate terminal, run there:  
1. `truffle migrate`  