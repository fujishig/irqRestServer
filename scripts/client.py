#!/usr/bin/env python3

""" client.py, a client to connect to irqRestServer

restServer must match serverhost and port specified in irqRestServer
"""

import requests
import json
import os

restServer = 'http://localhost:8001'

def _url(path):
    return restServer + path

def get_interrupts(start_time,end_time):
    """ Get the number of interrupts between start_time and end_time for all IRQs """
    attributes = {'start':start_time,'stop':end_time}
    req = requests.get(_url('/irqsummary'),params=attributes,
            headers={'content-type':'application/json','accept':'application/json'})
    #print(req.text)
    if 'irq_data' in req.json():
        irqdata = req.json()['irq_data']
        items = sorted(irqdata.items())
        print('{0:5} {1:>8} {2:>8}'.format('IRQ','CPU0','CPU1'))
        print('{0:5} {1:>8} {2:>8}'.format('-----','--------','--------'))
        for k,v in sorted(items):
            #print(k,v[0],v[1])
            print('{0:5} {1:8} {2:8}'.format(k,v[0],v[1]))
            #print("%s   %s" % [k,items[k]])
    if 'message' in req.json():
        print(req.json()['message'])

def set_affinity(irqId,affinity):
    """ Set the cpu affinity for specified irqId """
    attributes = {'cpu':affinity}
    req = requests.put(_url('/irqsummary/'+str(irqId)),data={'cpu' : affinity})
    if 'old affinity' in req.json():
        print("Affinity for",irqId,"changed from",req.json()['old affinity'],"to",req.json()['new affinity'])
    if 'message' in req.json():
        print(req.json()['message'])

def get_summary():
    """ get the number of interrupts since last reboot """
    get_interrupts(None,None)

if __name__ == "__main__":
    running = True 
    while running:
        print("Please enter an option from 1 to 3:\n\
    1 : get summary of interrupts since last reboot\n\
    2 : get summary of interrupts in a specified time\n\
    3 : set an IRQ's affinity to a specific CPU")
        option = input("enter: " )
        if option in ["1","2","3"]:
            if option == "1":
                get_summary() 
            if option == "2":
                start = input("Please enter a start date in mmddHHMM format: ")
                stop = input("Please enter a stop date in mmddHHMM format: ")
                get_interrupts(start,stop)
            if option == "3":
                irq = input("Please enter a valid IRQ number: ")
                cpu = input("Please enter a valide CPU number (enter 1 for cpu0, 2 for cpu1): ")
                set_affinity(irq,cpu)
            running = False 
        else:
            print("You didn't choose a valid option.")


