import subprocess
import os
import time
from datetime import datetime
#import matplotlib.pyplot as plt

def benignUE():
   # os.system("./build/nr-ue -c config/open5gs-ue.yaml  > log &")
    proc1 = subprocess.run(["./build/nr-ue -c config/open5gs-ue.yaml  > log &"],shell=True)
    #proc1.wait(timeout=5)
   # print(proc1.pid)
    #print(proc.stdout)
    time.sleep(10)
    proc2 = subprocess.Popen("ps -ef | grep './build/nr-ue -c config/open5gs-ue.yaml' | grep -v 'grep' | awk '{ printf $2 }'",shell=True,stdout=subprocess.PIPE)
    str1=str(proc2.stdout)
    pids=""
    for c in iter(lambda:proc2.stdout.read(1),b""):
        pids+=c.decode('utf-8')
    
    #print(pids)
    #print("this is the output -------- " + str1)
    subprocess.run(["kill","-9",pids])

    #proc1.kill()

def getTime(logLine):
    logLine=logLine.split()
    #print(logLine[1][:-1])
    timeString = logLine[1][:-1]
    format = "%H:%M:%S.%f"

    date_object = datetime.strptime(timeString, format)
    #print(date_object)

    return date_object


def timeDiff():
    lookup = "Connection setup for PDU"
    filename = "log"
    f=open(filename)
    lines=f.readlines()
    firstLine =lines[1]
    f.close()
    lastLine=lines[1]
    with open(filename) as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                lastLine = line
        myFile.close()
    
    startTime = getTime(firstLine)
    endTime = getTime(lastLine)
    delta = endTime - startTime
    deltams = delta.total_seconds()*1000 
    #print(deltams)
    return deltams


def startAttackScript(i):
    cmd = "bash attack" + str(i) + ".sh > attack" + str(i) + ".log &"
    proc1 = subprocess.run([cmd],shell=True)
    time.sleep(5)
    


def stopAttackScript(i):
    cmd = "ps -ef | grep 'attack" + str(i) + "' | grep -v 'grep' | awk '{ printf $2 }'"
    proc2 = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    str1=str(proc2.stdout)
    pids=""
    for c in iter(lambda:proc2.stdout.read(1),b""):
        pids+=c.decode('utf-8')

    subprocess.run(["kill","-9",pids])  


if __name__ == "__main__":
    times = []
    filename = "result"
    f=open(filename,"w")
    f.write("Starting the experiment...... \n")
    f.flush()
    
    for i in range (5):
        f.write("Sending reuquest from benign UE Case " + str(i+1) + "\n" )
        f.flush()
        benignUE()   
        ds = timeDiff()
        f.write("Time taken in request "+ str(i+1) + " - " + str(ds) + "\n")
        f.flush()
        times.append(ds)           

    for idx in range(1,6):
        f.write("Starting attack script " + str(idx) + "\n")
        f.flush()
        startAttackScript(idx)     
        time.sleep(2)
        for i in range(5):
            f.write("Sending reuquest from benign UE Case " + str(i+1) + "\n" )
            f.flush()
            benignUE()
            ds = timeDiff() 
            f.write("Time taken in request "+ str(i+1) + " - " + str(ds) + "\n")
            f.flush()
            times.append(ds)


    for i in range(1,6):
        stopAttackScript(i)
    
    os.system("clear")
    f.write("Times are - \n" )
    for i in times:
        f.write(str(i) + "\n")
    
    f.close()
    f=open("timings","w")
    for i in times:        
        f.write(str(i) + "\n")
    
    f.close()
