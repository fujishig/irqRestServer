#!/usr/bin/env python3

"""testLogFiles.py Script to populate log files needed for irqRestServer

irqRestServer depends on a simple script running every minute that extracts 
from /proc/interrupts for each Irq number, the number of interrupts on cpu0 
and number of interrupts on cpu1, separated by commas.  These are stored in a
specified log directory denoted by logPath in irqLog.py.

If the crontab script has not been running, you won't have any data, so this script
creates log files from the specified startDate to the specified endDate, one
per minute.   This is for testing purposes only.  Note that this will overwrite
existing files.  Also, the user that runs this will need write permissions on the log 
directory

irqs is a list of irqs that you want to generate logs for.  It's probably better to 
extract this automatically from /proc/interrupts, wip.

logPath in this script must match the logPath in irqLog.py

startDate is the start of your log files, endDate is the end.  The interrupt
values in startDate will be 0.

step0 and step1 are how much each cpu interrupt is incremented for each new
log file.  These are set to random integers between 0 and 10 in the loop
"""

import os
import datetime
import random

logPath = '/var/log/irqLogs/'
startDate = datetime.datetime(2014, 9, 8, 16, 44)
endDate = datetime.datetime(2014, 10, 31, 0, 0)
delta =  datetime.timedelta(minutes=1)
step0 = 1
step1 = 1
irqs = ["0","1","8","9","12","14","121"]
irqList = {}
for i in irqs:
    irqList[i] = [0,0]

# Make log directory if it doesn't already exist
try:
    os.makedirs(logPath)
except OSError:
    if not os.path.isdir(logPath):
        raise

d = startDate
while d <= endDate:
    fileName = os.path.join(logPath,d.strftime("%m%d%H%M")+".log")
    print("Creating/overwriting logfile: %s" % fileName)
    f = open(fileName,"w+")
    for i in irqs:
        # This is where you can change the step values
        step0 = random.randint(0,10)
        step1 = random.randint(0,10)
        irqList[i][0] += step0
        irqList[i][1] += step1
        f.write("%s,%d,%d\n" % (i,irqList[i][0],irqList[i][1]))
    f.close()
    d += delta

