#!/bin/bash

egrep '^[ ,1-9]+:' /proc/interrupts |awk '{print $1 ","$2","$3}' | sed 's/://' > /home/fujishig/logs/irqlogs/`date +%m%d%H%M`.log

