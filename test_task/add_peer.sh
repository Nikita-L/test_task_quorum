#!/bin/bash

subnet="172.13.0.0/16"
ips=("172.13.0.2" "172.13.0.3" "172.13.0.4" "172.13.0.5")
new_ip="172.13.0.5"

image=quorum

uid=`id -u`
gid=`id -g`
pwd=`pwd`

qd=qdata_4
mkdir -p $qd/{logs,keys}
mkdir -p $qd/dd/geth

enode=`docker run -u $uid:$gid -v $pwd/$qd:/qdata $image sh -c "/usr/local/bin/bootnode -genkey /qdata/dd/nodekey -writeaddress; cat /qdata/dd/nodekey"`
enode=`docker run -u $uid:$gid -v $pwd/$qd:/qdata $image sh -c "/usr/local/bin/bootnode -nodekeyhex $enode -writeaddress"`
enode_compl='enode://'$enode'@'$new_ip':30303?discport=0&raftport=50400'
echo $enode_compl

touch $qd/passwords.txt
account=`docker run -u $uid:$gid -v $pwd/$qd:/qdata $image /usr/local/bin/geth --datadir=/qdata/dd --password /qdata/passwords.txt account new | cut -c 11-50`

cp qdata_1/genesis.json $qd/genesis.json

nodelist=
for ip in ${ips[*]}
do
    sep=`[[ $ip != ${ips[0]} ]] && echo ","`
    nodelist=${nodelist}${sep}'"http://'${ip}':9000/"'
done

cat templates/tm.conf \
        | sed s/_NODEIP_/${new_ip}/g \
        | sed s%_NODELIST_%$nodelist%g \
              > $qd/tm.conf

docker run -u $uid:$gid -v $pwd/$qd:/qdata $image /usr/local/bin/constellation-node --generatekeys=qdata/keys/tm < /dev/null > /dev/null

# Get raft id
read -p "Enter the raft id: " RAFTID
echo $RAFTID

# Start node script
cat > $qd/start-node.sh <<EOF
#!/bin/bash

set -u
set -e

### Configuration Options
TMCONF=/qdata/tm.conf

GETH_ARGS="--datadir /qdata/dd --raft --raftjoinexisting $RAFTID --rpc --rpcaddr 0.0.0.0 --rpcapi admin,db,eth,debug,miner,net,shh,txpool,personal,web3,quorum --nodiscover --unlock 0 --password /qdata/passwords.txt"

if [ ! -d /qdata/dd/geth/chaindata ]; then
  echo "[*] Mining Genesis block"
  /usr/local/bin/geth --datadir /qdata/dd init /qdata/genesis.json
fi

echo "[*] Starting Constellation node"
nohup /usr/local/bin/constellation-node \$TMCONF 2>> /qdata/logs/constellation.log &

sleep 2

echo "[*] Starting node"
PRIVATE_CONFIG=\$TMCONF nohup /usr/local/bin/geth \$GETH_ARGS 2>>/qdata/logs/geth.log
EOF
chmod 755 $qd/start-node.sh


#docker run -u $uid:$gid -v $pwd/$qd:/qdata --network=test_task_quorum_quorum_net $image
docker run -d -u $uid:$gid --name test_task_quorum_node_4_1 -v $pwd/$qd:/qdata --network=test_task_quorum_quorum_net -p 22004:8545 --ip 172.13.0.5 $image
#docker run -u $uid:$gid -v $pwd/$qd:/qdata --network=test_task_quorum_quorum_net -p 22004:8545 --ip 172.13.0.5 $image