#!/usr/bin/env bash

mysql $1 < $2
exit $?
