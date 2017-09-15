#!/usr/bin/env python

import re
import os
import time
from settings import logPath, irqPath, irqWritePath

def processLogFile(logname,arr): 
    logRegex = re.compile(r'(\d+),(\d+),(\d+)')
    Total0 = 0
    Total1 = 0
    with open(logname) as logFile:
        for line in logFile:
            result = logRegex.search(line)
            [irqNum,cpu0num,cpu1num] = [result.group(1),result.group(2),result.group(3)]
            #[irqNum,cpu0num,cpu1num] = line.split(",")
            arr[irqNum]=[int(cpu0num),int(cpu1num)]
            Total0 += int(cpu0num)
            Total1 += int(cpu1num)
    arr["total"] = [Total0,Total1]    
    return(arr)

def returnIrqWindow(start,end):
    irqDict = {}
    irq2Dict = {}
    #print(logPath)
    filenames = next(os.walk(logPath))[2]
    filenames = [os.path.splitext(each)[0] for each in filenames]
    if start is not None:
        try:
            x1 = max(t for t in filenames if t!='' and int(t) <= int(start))
        except ValueError:
            return False
        startLogFile=os.path.join(logPath,x1 + ".log")
        processLogFile(startLogFile,irqDict)
    if end is None:
        end = time.strftime("%m%d%H%M")
    try:
        x2 = min(t for t in filenames if t!='' and int(t) >= int(end))
    except ValueError:
        return False
    stopLogFile=os.path.join(logPath,x2 + ".log")

    processLogFile(stopLogFile,irq2Dict)
    #print(irq2Dict)

    for key in irq2Dict:
        if key in irqDict:
            #print(key,irq2Dict[key][0])
            irq2Dict[key][0] = irq2Dict[key][0] - irqDict[key][0]
            irq2Dict[key][1] = irq2Dict[key][1] - irqDict[key][1]
    #printt(irq2Dict)
    return(irq2Dict)

def irqGetAffinity(num):
    irqNum = str(num)
    irqList = next(os.walk(irqPath))[1] 
    if irqNum in irqList: 
        irqFile = os.path.join(irqPath,str(num),"smp_affinity")
        with open(irqFile) as irqFile:
            return(irqFile.read().rstrip())
    else:
        return False

def irqModifyAffinity(num,cpu):
    irqNum = str(num)
    irqList = next(os.walk(irqPath))[1]
    cpuList = ['1','2']
    if irqNum in irqList and cpu in cpuList:
        irqFile = os.path.join(irqWritePath,str(num),"smp_affinity")
        with open(irqFile,"w") as irqFile:
            irqFile.writelines(str(cpu))
        return True
    else:
        return False


