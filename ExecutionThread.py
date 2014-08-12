import threading, Queue, os, time
from util.Settings import GpioDict, IntensityDict, WireGpioDict, RASPI, PatternDict

DEFAULT_FREQUENCY = 120

TIME_TO_LIGHT_OFFSET    = 0
TIME_TO_WAIT_OFFSET     = 1

class ExecutionThread(threading.Thread):
    def __init__(self, pattern, intensity, log):
        super(ExecutionThread,self).__init__()
        self.log = log
        self.CALLING_CLASS = "ExecutionThread"
        self.__log("Setting up Execution Thread")
        self.pattern = pattern
        self.stoprequest = threading.Event()
        self.intensity = intensity
    
    def __log(self,message):
        self.log.LOG(self.CALLING_CLASS, message)
        
    def run(self):
        self.__log("Starting the thread")
        numOfGpios = self.pattern.GetRequiredColors()
        colorList = self.pattern.GetColorList()
        pwmDict = self.pattern.GetPwmSequenceDict()
        strobeIntensity = IntensityDict[self.intensity]
    
        gpioPinList = list()
        strobePatternList = list()
        wiringGpioPinList = list()
        
        if (len(colorList) == len(pwmDict)):
            for color in colorList:
                index = colorList.index(color)
                strobePattern = pwmDict[index]
                
                pin = GpioDict[color]
                wiringPin = WireGpioDict[color]
                       
                gpioPinList += [pin]
                wiringGpioPinList += [wiringPin]
                strobePatternList += [strobePattern]
        else:     
            self.__log("Invalid configuration")
            self.join()
            
        configurationString = "\n======================= PWM Configuration ============================\n"
        for ind, tmpPin in enumerate(gpioPinList):
            tmpPattern = strobePatternList[ind]
            tmpColor = colorList[ind]
            configurationString += "\n\tGPIO %d: Color- %s, Pin- %d, Brightness- %d, %d, Pattern- %s"%(ind, tmpColor, tmpPin, self.intensity, strobeIntensity, str(tmpPattern))
            
        configurationString += "\n\n=======================================================================\n"
        self.__log(configurationString)
        
        pinString = ""
        for pin in wiringGpioPinList:
            pinString += str(pin) + " "
        
        for pad in range(0,3-len(wiringGpioPinList)):
            pinString += "-1 "
            
        pinString = pinString[:-1]
        self.__log("Pin string: %s"%pinString)
        executionString = "sudo /bin/pwm %s %d %d &"%(pinString, strobeIntensity, PatternDict[self.pattern.GetName()])
        self.__log("Execution String : %s"%executionString)
        if RASPI:
            os.system(executionString)
        while not self.stoprequest.isSet():
            time.sleep(.5)
            
        if RASPI:            
            os.system("sudo pkill pwm")
##########################################################################
### This code causes a virtual memory leak and will crash the thread.    #
### The virtual memory allocated by gpio.start() is never released       #
### and therefore increments indefinately until all memory is consumed.  #
### Looking in the C Code of the RPi.GPIO project, the issue is          #
### dealloc() is never called. See the source code for more info.        #
### This code is kept here to show a more basic overview of what is      #
### happening.                                                           #
##########################################################################
#            for ind,gpio in enumerate(gpioList):                        #
#                timingSequence = strobePatternList[ind]                 #
#                for timingPair in timingSequence:                       #
#                    onTime = timingPair[0]                              #
#                    offTime = timingPair[1]                             #
#                    if RASPI:                                           #
#                        gpio.start(strobeIntensity)                     #
#                    time.sleep(onTime)                                  #
#                    if RASPI:                                           #
#                        if len(timingSequence) != 1 or offTime != 0:    #
#                            gpio.stop()                                 #
#                            time.sleep(offTime)                         #
##########################################################################

    def join(self, timeout=None):
        self.__log("JOIN CALLED")
        self.stoprequest.set()
        time.sleep(.25)
        if RASPI:
            os.system("sudo pkill pwm")
        super(ExecutionThread,self).join(timeout)
        