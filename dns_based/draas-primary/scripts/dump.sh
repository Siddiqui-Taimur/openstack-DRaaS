#!/usr/bin/env bash

mysqldump -B $1 > $2
exit $?