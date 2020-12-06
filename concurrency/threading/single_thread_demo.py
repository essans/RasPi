!/usr/bin/python3.7

# https://realpython.com/intro-to-python-threading/

import os
import threading
import time
from datetime import datetime

def log(message,console='y'):
    mode = "a"

    if message == "clear":
            mode = 'w'

    with open("log_threading.log",mode) as f:

        if message == "start":
            message = "------------ START ------------"

        f.write(str(datetime.now()).split(".")[0]+"|"+message+"\n")
        
        if console in ["Y",'y']:
            print(message)


def thread_function(name):
    log("Thread {} fucntion starting".format(name))

    time.sleep(2)

    log("Thread {} function running...".format(name))

    time.sleep(2)

    log("Thread {} function finishing".format(name))



if __name__ == "__main__":

    log("start")
    time.sleep(1)

    log("Main | running & before creating thread")
    time.sleep(1)    

    x = threading.Thread(target=thread_function, args=(1,),daemon=None)
    log(str(x))    

    log("Main | before running thread(s)")
    x.start()
    log(str(x))
    time.sleep(1)
    
    #log("Main | wait for the thread(s) to finish"
    #x.join()

    time.sleep(2)
    
    log("Main | continues to run")
    
    log("Main | all done")
