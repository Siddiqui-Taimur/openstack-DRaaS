#!/usr/bin/env bash

sudo chmod 777 scripts/*
if [ -d /recover/draas ]; then
echo "Draas Recover Directory Already Exists";
else
    mkdir /recover
    mkdir /recover/draas
    chmod -R 777 /recover
    echo "Draas Recover Directory Created"
fi
if [ -d /var/log/draas ]; then
echo "Draas Log Directory Already Exists";
else
    mkdir /var/log/draas
    chmod 777 /var/log/draas
    echo "Draas Directory Created"
fi
if [ -f /var/log/draas/draas.log ]; then
echo "Draas Log File Already Exists";
else
    touch /var/log/draas/draas.log
    chmod 777 /var/log/draas/draas.log
    echo "Draas Log File Created"
fi
if [ -d /etc/draas ]; then
echo "Draas Configuration Directory Already Exists";
else
    mkdir /etc/draas
    chmod 777 /etc/draas
    echo "Draas Configuration Directory Created"
fi
if [[ -f /etc/draas/keystone.conf && -f /etc/draas/draas.conf ]]; then
echo "Draas Configurations Files Already Exists";
else
    cp keystone.conf draas.conf /etc/draas
    echo "Draas Configuration Files Copied"
fi
sudo chmod 777 /var/log/mysql