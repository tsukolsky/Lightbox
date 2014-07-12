import threading, Queue, os, time
from util.Settings import GpioDict, IntensityDict

RASPI = True
if RASPI:
    import RPi.GPIO as RasIo

DEFAULT_FREQUENCY = 120

TIME_TO_LIGHT_OFFSET    = 0
TIME_TO_WAIT_OFFSET     = 1

class ExecutionThread(threading.Thread):
    def __init__(self, pattern, intensity):
        super(ExecutionThread,self).__init__()
        print "Setting up Execution Thread"
        self.pattern = pattern
        self.stoprequest = threading.Event()
        self.intensity = intensity
        
    def run(self):
        print "Starting the thread"
        numOfGpios = self.pattern.GetRequiredColors()
        colorList = self.pattern.GetColorList()
        pwmDict = self.pattern.GetPwmSequenceDict()
        strobeIntensity = IntensityDict[self.intensity]
        
        if RASPI:
            RasIo.setmode(RasIo.BOARD)
        # Put together the GPIO list ------------------------------
        ## Case 1: pwmDict length == number of colors
        ## Case 2: pwmDict length > number of colors --> Make # GPIOs with the same pin to simulate # colors
        ## Case 3: Not sure
    
        gpioPinList = list()
        gpioList = list()
        strobePatternList = list()
        
        if (len(colorList) == len(pwmDict)):
            for color in colorList:
                index = colorList.index(color)
                strobePattern = pwmDict[index]
                
                pin = GpioDict[color]
                if RASPI:
                    RasIo.setup(pin, RasIo.OUT)
                    gpio = RasIo.PWM(pin,DEFAULT_FREQUENCY)
                    gpioList += [gpio]
                else:
                    gpioList += [0] 
                       
                gpioPinList += [pin]
                strobePatternList += [strobePattern]
        else:     
            print "Invalid configuration"
            self.join()
            
        configurationString = "======================= PWM Configuration ============================\n"
        for ind, gpio in enumerate(gpioList):
            tmpPin = gpioPinList[ind]
            tmpPattern = strobePatternList[ind]
            tmpColor = colorList[ind]
            configurationString += "\n\tGPIO %d: Color- %s, Pin- %d, Brightness- %d, Pattern- %s"%(ind, tmpColor, tmpPin, self.intensity, str(tmpPattern))
            
        configurationString += "\n\n=======================================================================\n"
        print configurationString
        
        while not self.stoprequest.isSet():
            ## Loop through each GPIO, turn it on for specified time, then off
            for ind,gpio in enumerate(gpioList):
                print "BEEP"
                timingSequence = strobePatternList[ind]
                for timingPair in timingSequence:
                    onTime = timingPair[0]
                    offTime = timingPair[1]
                    if RASPI:
                        gpio.start(strobeIntensity)
                    time.sleep(onTime)
                    if RASPI:
                        gpio.stop()
                    time.sleep(offTime)
                    
    def join(self, timeout=None):
        print "JOIN CALLED"
        self.stoprequest.set()
        time.sleep(.5)
        RasIo.cleanup()
        super(ExecutionThread,self).join(timeout)
        