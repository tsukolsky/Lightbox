from util.Events import Event
import threading

class DurationTrigger(threading.Thread):
    def __init__(self, id, timeInSeconds = 0, log = None):
        super(DurationTrigger,self).__init__()
        self.__id = id
        self.__durationTime = timeInSeconds
        self.__running = False
        self.log = log
        self.CALLING_CLASS = "DurationTrigger %d"%self.__id
        self.DurationTimeUpdate = Event()
        self.DurationCompleted = Event()
        self.stoprequest = threading.Event()
       
    def __log(self, message):
        if self.log != None:
            self.log.LOG(self.CALLING_CLASS, message)
             
    def GetId(self):
        return self.__id
    
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
            self.DurationTimeUpdate(tmpTime)
            time.sleep(1)
            tmpTime -= 1
        
        self.__log("Out of while loop")
        ## Raise event if time based stop
        if not self.stoprequest.isSet():
            self.__log("Stopped because of user stop")
            self.DurationTimeCompleted()
        else:
            self.__log("Stopped because of time trigger completion")
            self.DurationTimeUpdate(tmpTime)
            
        self.__running = False
        
    def join(self, timeout=None):
        self.__log("Join Join Join")
        self.stoprequest.set()
        time.sleep(.2)
        super(DurationTrigger,self).join(timeout)
        
    