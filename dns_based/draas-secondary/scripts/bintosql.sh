#!/usr/bin/env bash

mysqlbinlog /etc/draas/mysql-bin.000001.old -d $1 > $2
