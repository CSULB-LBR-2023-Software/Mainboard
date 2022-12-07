#!/bin/bash

stop=false
while [ "$stop" = false ]
do
python3 server.py "$(grep "XX4XXX" radio.txt)" &

if ! python3 checkExit.py "$(grep "XX5XXX" radio.txt)" ; then
python3 client.py
stop=true
echo "Exiting loop"
break
fi

python3 client.py

done



