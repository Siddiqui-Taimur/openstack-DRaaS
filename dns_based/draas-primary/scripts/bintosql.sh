#!/usr/bin/env bash

file="$(find /etc/draas/ -name '*000*')"
if [ ! -z "$file" ]; then
echo 'Files found'
mysqlbinlog -d $1 $file > $2
fi
