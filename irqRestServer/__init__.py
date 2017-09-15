#!/usr/bin/env python

import os
import subprocess
import re
from flask import Flask, request, jsonify 
from irqLog import returnIrqWindow, irqGetAffinity, irqModifyAffinity
from datetime import datetime
from settings import SERVER_HOST, SERVER_PORT

app = Flask(__name__)

def lastReboot():
    output = subprocess.check_output(["uptime", "-s"])
    m = re.search("-(\d+)-(\d+)\s+(\d+):(\d+):",output)
    if m:
        restart = m.group(1)+m.group(2)+m.group(3)+m.group(4)
        return restart
    else:
        return False

def validateDate(d):
    try:
        if d != datetime.strptime(d,"%m%d%H%M").strftime("%m%d%H%M"):
            raise ValueError
        return True
    except:
        return False

#@app.route('/') 
#def main():
    #return 'Hello, world!'

@app.route('/irqsummary', methods=['GET'])
def irqsummary():
    reboot = lastReboot()
    if 'start' in request.values:
        startDate = request.values['start']
        if not validateDate(startDate):
            return jsonify({'message':'start is not a valid format (%m%d%H%M)'}) 
        if reboot > startDate:
            return jsonify({'message':'start is prior to last reboot: '+reboot})
        if 'stop' in request.values:
            stopDate = request.values['stop']
            if not validateDate(stopDate):
                return jsonify({'message':'stop is not a valid format (%m%d%H%M)'}) 
            if startDate > stopDate:
                return jsonify({'message':'start is greater than stop'})
            if returnIrqWindow(startDate,stopDate):
                return jsonify({'message':'Success','irq_data':returnIrqWindow(startDate,stopDate)})
            else:
                return jsonify({'message':'Not enough data to produce interrupt count'})
        else:
            if returnIrqWindow(startDate,None):
                return jsonify({'message':'IRQ data from '+startDate,'irqData':returnIrqWindow(startDate,None)})
            else:
                return jsonify({'message':'Not enough data to produce interrupt count'})
    else:
        return jsonify({'message':"No start date specified.  Returning values since last reboot: "+reboot, 
                'irq_data':returnIrqWindow(None,None)})

@app.route('/irqsummary/<int:irq_id>', methods=['GET'])
def get_irq(irq_id):
    affinity = irqGetAffinity(irq_id)
    if affinity:
        return jsonify({'irq_id':irq_id,'current affinity':affinity })
    else:
        return jsonify({'message':'invalid irq-id'})

@app.route('/irqsummary/<int:irq_id>', methods=['PUT'])
def update_affinity(irq_id):
    current_aff = irqGetAffinity(irq_id)
    print(request.values.keys())
    if current_aff:
        if 'cpu' in request.values:
            cpuNum = request.values['cpu']
            if irqModifyAffinity(irq_id,cpuNum):
                return jsonify({'message':'Affinity changed','old affinity':current_aff,'new affinity':cpuNum})
            else:
                return jsonify({'message':'Invalid cpu specified'})
        else:
            return jsonify({'message':'No cpu identified'})
    else:
        return jsonify({'message':'Invalid irq-id specified'})



if __name__ == '__main__':
    app.run(host=SERVER_HOST,port=SERVER_PORT)
