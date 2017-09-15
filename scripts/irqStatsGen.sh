#!/bin/bash

# Run as crontab every minute.  Make sure to create log directory first.

egrep '^[ ,1-9]+:' /proc/interrupts |awk '{print $1 ","$2","$3}' | sed 's/://' > /var/log/irqLogs/`date +%m%d%H%M`.log

