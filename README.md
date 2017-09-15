# irqRestServer

Simple flask REST server to expose IRQ affinity information from /proc/interrupts on a linux machine with 2 cpus.  
WARNING:  there is no authentication involved so this is for testing purposes only

## Getting Started

Python and pip are required before installation.

### Installing

Setup:
```
python setup.py install
```

Run from command line:
```
./run.py
```

### Scripts 

irqStatsGen.sh should be put in a crontab.  It grabs the numeric IRQs from /proc/interrupts, as well as the number of interrupts for the first and second cpus in a comma separated list,
then exports that to a log file in the specified directory named 'date +%m%d%H%M'
```
* * * * * /directory-to-script/irqStatsGen.sh
```

testLogFiles.py will populate dummy log files with IRQ info for testing purposes.  

client.py is a simple REST client to access the api

