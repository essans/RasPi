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
    log("Thread {} fucntion starting\n".format(name))

    time.sleep(3)

    log("Thread {} function running...\n".format(name))

    time.sleep(3)

    log("Thread {} function finishing\n".format(name))



if __name__ == "__main__":

    log("start\n")
    time.sleep(2)

    log("Main | running & before creating thread\n")
    time.sleep(5)    

    x = threading.Thread(target=thread_function, args=(1,),daemon=None)
    log(str(x))    

    time.sleep(3)
    
    log("Main | before running thread(s)\n")
    
    time.sleep(5)
    
    x.start()
    log(str(x))
    
    time.sleep(2)
    
    #log("Main | wait for the thread(s) to finish\n"
    #x.join()

    time.sleep(2)
       
    log("Main | continues to run\n")
    
    log("Main | all done\n")
