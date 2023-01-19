#!/bin/bash

cat radio.txt | sed -n -e 's/^.*\(XX4XXX \)/\1/p' | python3 server.py &

python3 client.py





