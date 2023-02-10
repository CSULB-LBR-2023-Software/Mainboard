#!/bin/bash

cat radio.txt | sed -u -n -e 's/^.*\(XX4XXX \)/\1/p' | python3 radioMp.py
