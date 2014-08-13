from util.Events import Event
import threading, time , os, sys

class DurationTrigger(threading.Thread):
    def __init__(self, timeInSeconds = 0, log = None):
        super(DurationTrigger,self).__init__()
        self.__durationTime = timeInSeconds
        self.__running = False
        self.log = log
        self.CALLING_CLASS = "DurationTrigger"
        self.DurationTimeUpdated = Event()
        self.stoprequest = threading.Event()
        self.pauserequest = threading.Event()
       
    def __log(self, message):
        if self.log != None:
            self.log.LOG(self.CALLING_CLASS, message)
             
    def IsRunning(self):
        return self.__running
    
    def GetDuration(self):
        return self.__durationTime
    
    def SetDuration(self, timeInSeconds = 0):
        self.__log("SetDuration")
        if timeInSeconds > 0:
            self.__log("Setting duration to %d"%timeInSeconds)
            self.__durationTime = timeInSeconds
            return True
        else:
            return False
    
    def run(self):
        self.__log("Run->Starting while loop")
        self.__running = True
        tmpTime = self.__durationTime
        
        ## Sleep for a second, then decrement the counter.
        while (tmpTime > 0 and not self.stoprequest.isSet()):
            if (self.pauserequest.isSet()):
                time.sleep(1)
            else:
                self.DurationTimeUpdated(tmpTime)
                time.sleep(1)
                tmpTime -= 1
        
        self.__log("Out of while loop")
        ## Raise event if time based stop
        if not self.stoprequest.isSet():
            self.__log("Stopped because of user stop")
        else:
            self.__log("Stopped because of time trigger completion")
            
        self.DurationTimeUpdated(tmpTime)
        self.__running = False
     
    def Pause(self):
        self.pauserequest.set()
        
    def Resume(self):   
        self.pauserequest.clear()
        
    def join(self, timeout=None):
        self.__log("Join Join Join")
        self.stoprequest.set()
        time.sleep(.2)
        super(DurationTrigger,self).join(timeout)
        
    