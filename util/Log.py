import os, sys, time, datetime
import inspect

class Log():
	def __init__(self, terminalPrint = False):
		fileLoc = inspect.stack()[0][1]
		withoutUtil = fileLoc.split("util")
		timestamp = time.time()
		makeTime = datetime.datetime.fromtimestamp(timestamp).strftime('__%Y-%m-%d__%H:%M:%S')
		self.__logFile = withoutUtil[0] + "logs/log" + makeTime + ".log"
		self.__terminalPrint = terminalPrint
		self.LOG("Log","Log Initialized")
		
	def LOG(self,callingClass="",message=""):
		if (len(callingClass) == 0 or len(message) == 0):
			return
		timestamp = time.time()
		callTime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
		logMessage = "%s:   %s:   %s"%(callTime, callingClass, message)
		if self.__terminalPrint:
			print logMessage
			of = open(self.__logFile,'a')
			of.write(logMessage)
			of.close()
		
	def GetLogPath(self):
		return self.__logFile