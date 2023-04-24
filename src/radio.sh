#!/bin/bash

# Author: Nick Fan
# Date: 3/29/2023

radio=false
debug=false
showUsage=false

usage() {
	echo LBR 2023 Payload Radio Processing Module$'\n'
	echo Usage: $0 [arguments] ... [option]$'\n'
	echo Arguments:
	echo $'  -r\tRun script using radio mode. Data will be piped from Multimon-ng.'
	echo $'  -d\tRun script using debug mode. Data will be piped from its argument as a file.'	
	echo $'  -h\tShow usage.'
}

args=0

while getopts "rd:h" option; do 
	case $option in 
		r)
			radio=true
			((args++))
			;;
		d)
			file=$OPTARG
			if [ -z "$file" ]; then
				echo 'Error: missing file name for debug mode.' >&2
				exit 1
			fi
			debug=true
			((args++))	
			;;
		h)
			showUsage=true
			((args++))
			;;
		*)
			echo 'Error: Invalid argument set passed.' >&2
			exit 1
	esac
done

if [ "$args" -gt 1 ]; then
	echo 'Error: Too many arguments passed.' >&2
	exit 1
fi

if [ "$showUsage" = true ]; then
	usage
	exit 0
fi

if [ "$radio" = true ]; then
	echo Radio mode selected. Beginning operations...	
elif [ "$debug" = true ]; then
	echo Debug mode selected with file $file. Beginning operations...
fi

if [ "$args" -lt 1 ]; then
	echo No options selected, defaulting to radio mode. Beginning operations...
	radio=true
fi

if [ "$radio" = true ]; then
	python3 predeployment.py
	rtl_fm -f 144.390M -s 22050 | multimon-ng -t raw -a AFSK1200 -f alpha /dev/stdin | sed -u -n -e 's/^.*\(KN6WUV \)/\1/p' | python3 radio_mp.py
elif [ "$debug" = true ]; then
	cat $file | sed -u -n -e 's/^.*\(KN6WUV \)/\1/p' | python3 radio_mp.py
fi
