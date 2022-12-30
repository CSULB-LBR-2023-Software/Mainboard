#!/bin/bash

stop=false
while [ "$stop" = false ]
do
python3 server.py "$(sed -n -e 's/^.*\(XX4XXX \)/\1/p' radio.txt)" &

if ! python3 checkExit.py "$(sed -n -e 's/^.*\(XX5XXX \)/\1/p' radio.txt)" ; then
python3 client.py
stop=true
echo "Exiting loop"
break
fi

python3 client.py

done



