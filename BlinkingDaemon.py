import os, time
from util.Settings import GpioDict, IntensityDict
RASPI = False
if RASPI:
    import RPi.GPIO as RasIo

DEFAULT_FREQUENCY = 120

TIME_TO_LIGHT_OFFSET    = 0
TIME_TO_WAIT_OFFSET     = 1

class BlinkingDaemon():
    def __init__(self, pattern, intensity, log):
        self.log = log
        self.CALLING_CLASS = "BlinkingDaemon"
        self.__log("Setting up Blinking Daemon")
        self.pattern = pattern
        self.__run = False
        self.intensity = intensity
    
    def __log(self,message):
        self.log.LOG(self.CALLING_CLASS, message)
        
    def Run(self):
        self.__log("Starting the daemon")
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
            self.__log("Invalid configuration")
            self.__running = False
            return
            
        configurationString = "\n======================= PWM Configuration ============================\n"
        for ind, gpio in enumerate(gpioList):
            tmpPin = gpioPinList[ind]
            tmpPattern = strobePatternList[ind]
            tmpColor = colorList[ind]
            configurationString += "\n\tGPIO %d: Color- %s, Pin- %d, Brightness- %d, %d, Pattern- %s"%(ind, tmpColor, tmpPin, self.intensity, strobeIntensity, str(tmpPattern))
            
        configurationString += "\n\n=======================================================================\n"
        self.__log(configurationString)
        self.__running = True
        while self.__running:
            ## Loop through each GPIO, turn it on for specified time, then off
            for ind,gpio in enumerate(gpioList):
                timingSequence = strobePatternList[ind]
                for timingPair in timingSequence:
                    onTime = timingPair[0]
                    offTime = timingPair[1]
                    if RASPI:
                        gpio.start(strobeIntensity)
                    time.sleep(onTime)
                    if RASPI:
                        if len(timingSequence) != 1 or offTime != 0:
                            gpio.stop()
                            time.sleep(offTime)
                    
    def Halt(self):
        self.__running = False
        self.__log("Halt Called.")
        
        