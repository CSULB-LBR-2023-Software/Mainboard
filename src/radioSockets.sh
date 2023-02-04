#!/bin/bash

cat radio.txt | sed -u -n -e 's/^.*\(XX4XXX \)/\1/p' | python3 receiver.py | python3 server.py &

sleep 5

python3 client.py





