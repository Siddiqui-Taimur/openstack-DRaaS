#!/usr/bin/env bash

sudo ifconfig eth0 down
sleep 120
echo 'Stopped'
sudo ifconfig eth0 up
