# irqRestServer

Simple flask REST server to expose IRQ affinity information from /proc/interrupts on a linux machine with 2 cpus.  
WARNING:  there is no authentication involved so this is for testing purposes only.

In order to get the number of interrupts in a window, we had to find a way to take the information from /proc/interrupts
and store it.  I tried using something like sar from sysstat but even after setting it to collect interrupt statistics,
like vmstat, it only did interrupts per second in a window.  To simplify things I just took a bash script to extract data from 
/proc/interrupts on a one minute interval, putting it into flat files instead of a database.  The REST server will look at the
file closest to the start time and end times and calculate the difference.  Since /proc/interrupts gets reset on system 
reboot, if start is prior to the last reboot, it returns a message saying so.  Ideally it would calculate the total number
of interrupts before and after reboot, but depending on the window that would also require logic to do this for every reboot
in the window.  

The REST API supports:

1. GET on /irqsummary:
Takes two parameters, 'start' and 'stop.'  returns the number of interrupts for all valid IRQs per CPU within the window.
2. GET on /irqsummary/IRQID:
Returns the current affinity of the specified irq-id.
3. PUT on /irqsummary/IRQID:
Takes one key, 'cpu' and changes the affinity of the specified irq-id.  The only valid values are 1 and 2, corresponding
to CPU0 and CPU1.

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

Run via supervisor:
```
apt-get install supervisor
```
Copy the irqRestServer.conf file in the scripts directory to /etc/supervisor/conf.d
Change the logfile and command location as needed
Reload supervisor:
```
supervisorctl reread
supervisorctl update
```

### Scripts 

irqStatsGen.sh should be put in a crontab.  It grabs the numeric IRQs from /proc/interrupts, as well as the number of interrupts for the first and second cpus in a comma separated list,
then exports that to a log file in the specified directory named 'date +%m%d%H%M'
```
* * * * * /directory-to-script/irqStatsGen.sh
```

testLogFiles.py will populate dummy log files with IRQ info for testing purposes.  

irqRestServer.conf is a configuration file to run the flask server via supervisor

client.py is a simple REST client to access the api:
```
Please enter an option from 1 to 3:
    1 : get summary of interrupts since last reboot
    2 : get summary of interrupts in a specified time
    3 : set an IRQ's affinity to a specific CPU
```



