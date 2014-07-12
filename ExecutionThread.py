import threading, Queue, os, time
#import RPi.GPIO as GPIO
from util.Settings import GpioDict, IntensityDict, CONTINOUS_PATTERN

UBUNTU = True

FREQUENCY_OFFSET        = 0
TIME_TO_LIGHT_OFFSET    = 1
TIME_TO_WAIT_OFFSET     = 2

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
        
        print colorList
        print pwmDict
        # Put together the GPIO list ------------------------------
        ## Case 1: pwmDict length == number of colors
        ## Case 2: pwmDict length > number of colors --> Make # GPIOs with the same pin to simulate # colors
        ## Case 3: Not sure
    
        gpioPinList = list()
        gpioList = list()
        gpioFreqList = list()
        gpioTimeList = list()
        gpioWaitTimeList = list()
        
        if (len(colorList) == len(pwmDict)):
            print "Color list and pwmDict correspond"
            print "Color list len = %d"%len(colorList)
            for color in colorList:
                print "Color %s"%color
                index = colorList.index(color)
                freq = pwmDict[index][FREQUENCY_OFFSET]
                timeToLight = pwmDict[index][TIME_TO_LIGHT_OFFSET]
                if (timeToLight == -1):
                    print "CONTINOUS PATTERN"
                    timeToLight = 1              # I literally just picked this number for no reason
                    
                timeToWait = pwmDict[index][TIME_TO_WAIT_OFFSET]
                
                pin = GpioDict[color]
                if not UBUNTU:
                    gpio = GPIO.PWM(pin,freq)
                    gpioList += [gpio]
                else:
                    gpioList += [0] 
                       
                gpioFreqList += [freq]
                gpioPinList += [pin]
                gpioTimeList += [timeToLight]
                gpioWaitTimeList += [timeToWait]
        elif (len(colorList) < len(pwmDict)):
            color = colorList[0]
            for key, pwmList in pwmDict.iteritems():
                freq = pwmList[FREQUENCY_OFFSET]
                timeToLight = pwmList[TIME_TO_LIGHT_OFFSET]
                if (timeToLight == -1):
                    print"CONTINOUS PATTERN"
                    timeToLight = 1
                
                timeToWait = pwmList[TIME_TO_WAIT_OFFSET]
                pin = GpioDict[color]
                
                if not UBUNTU:
                    gpio = GPIO.PWM(pin, freq)
                    gpioList += [gpio]
                else:
                    gpioList += [0]
                    
                gpioFreqList += [freq]
                gpioPinList += [pin]
                gpioTimeList += [timeToLight]
                gpioWaitTimeList += [timeToWait]
        elif (len(colorList) == 2 and len(pwmDict) == 0):
            print "Found the 2Hz 25% 4-3 alternating"
            return
        else:     
            print "Invalid configuration"
            self.join()
            
        configurationString = "======================= PWM Configuration ============================\n"
        for ind, gpio in enumerate(gpioList):
            tmpColor = ""
            tmpFreq = gpioFreqList[ind]
            tmpPin = gpioPinList[ind]
            tmpDisplayTime = gpioTimeList[ind]
            tmpOffTime = gpioWaitTimeList[ind]
            if (len(colorList) != len(pwmDict)):
                tmpColor = colorList[0]
            else:
                tmpColor = colorList[ind]
            configurationString += "\n\tGPIO %d: Color- %s, Pin- %d, Frequency- %d, Display Time- %d, Off Time- %d"%(ind, tmpColor, tmpPin, tmpFreq, tmpDisplayTime, tmpOffTime)
        configurationString += "\n\n=======================================================================\n"
        print configurationString
        
        while not self.stoprequest.isSet():
            ## Loop through each GPIO, turn it on for specified time, then off
            for ind,gpio in enumerate(gpioList):
                print "BEEP"
                displayTime = gpioTimeList[ind]
                offTime = gpioWaitTimeList[ind]
                if not UBUNTU:
                    gpio.start(IntensityDict[self.intensity])
                time.sleep(displayTime)
                if not UBUNTU:
                    gpio.stop()
                time.sleep(offTime)
                
    def join(self, timeout=None):
        print "JOIN CALLED"
        self.stoprequest.set()
        super(ExecutionThread,self).join(timeout)
        