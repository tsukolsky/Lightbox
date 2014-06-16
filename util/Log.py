import os, sys
import inspect

class Log():
	def __init__(self):
		print "Logger"

		fileLoc = inspect.stack()[0][1]
		withoutUtil = fileLoc.split("util")
		self.__logFile = withoutUtil[0] + "log.txt"
		print self.__logFile