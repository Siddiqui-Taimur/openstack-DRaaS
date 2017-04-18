#!/bin/bash

mysqlbinlog /etc/draas/mysql-bin.000001 -d $1 > $2