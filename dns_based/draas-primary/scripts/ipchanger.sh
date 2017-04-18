#!/usr/bin/env bash

sudo ifconfig eth0 $1 netmask $2
sudo route add default gw $3
