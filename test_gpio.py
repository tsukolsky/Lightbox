import os, time, sys
import RPi.GPIO as RasIo

RasIo.setmode(RasIo.BOARD)
RasIo.setup(7,RasIo.OUT)

redStrobe = RasIo.PWM(7,2)
redStrobe.start(100)

time.sleep(5)
redStrobe.stop()