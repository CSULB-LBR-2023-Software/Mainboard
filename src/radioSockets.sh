#!/bin/bash

stop=false
while [ "$stop" = false ]
do
python3 server.py "$(grep "XX4XXX" radio.txt)" &
python3 client.py
python3 checkExit.py "$(grep "XX5XXX" radio.txt)"

if [ $? -ne 0 ]
then
echo $?
stop=true
echo "Exiting loop"
break
fi

done



