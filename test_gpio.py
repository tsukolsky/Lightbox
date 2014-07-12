import os, time, sys
from RPi.GPIO import  GPIO

redStrobe = GPIO.PWM(7,2)
redStrobe.start(100)

time.sleep(5)
redStrobe.stop()