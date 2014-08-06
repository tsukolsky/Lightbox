import os, sys, time
from util.Settings import RASPI

class PatternManager():
    def __init__(self, log = None):
        self.log = log
        self.CALLING_CLASS = "PatternManager"
        if RASPI:
            self.__pFile = "/home/pi/Desktop/Lightbox/default_patterns.pat"
        else:
            self.__pFile = os.path.dirname(os.path.abspath(__file__)) + '/default_patterns.pat'
            print self.__pFile
            
    def __log(self, message):
        if self.log != None:
            self.log.LOG(self.CALLING_CLASS, message)
            
    def __openPFile(self):
        if not os.path.exists(self.__pFile):
            os.system("touch %s"%self.__pFile)
        self.__fh = open(self.__pFile, 'r')
        return self.__fh
    
    def GetPatterns(self):
        self.__fh = self.__openPFile()    
            
        return None
    
    
if __name__ == "__main__":
    man = PatternManager()
    man.GetPatterns()