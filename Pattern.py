import os, sys, time
from util.Settings import Colors, ColorsByIndex

#from RPGPIO import PWM
PWM_DICT_FREQUENCY  = 0
PWM_DICT_DUTY       = 1
PWM_DICT_SLEEP_TIME = 2

class Pattern():
    def __init__(self, name = "", des = "", default = False, colorList = list(), numRequired = -1, pwmDict = dict()):
        self.__name = name
        self.__description = des
        self.__default = default
        self.__colorList = colorList
        self.__requiredColors = numRequired
        self.__pwmSequenceDict = pwmDict
    
    def CanStart(self):
        # Check colors
        if  len(self.__colorList) != 0:
            for color in self.__colorList:
                if color == ColorsByIndex[Colors.Empty]:
                    print "Pattern: Not all colors configured"
                    return False
                else:
                    print "Color %d is %s"%(self.__colorList.index(color), color)
        # Check PWM sequence
        return True    
    
    def ClearColors(self):
        tmpList = list()
        for color in self.__colorList:
            tmpList += [ColorsByIndex[Colors.Empty]]
            
        self.__colorList = tmpList
            
    def CopyPattern(self,name = None, description = None):
        retPattern = Pattern()
        #print description
        # Copy name
        if name == None:
            retPattern.SetName(self.__name)
        else:
            retPattern.SetName(name)
        
        if description == None:
            retPattern.SetDescription(self.__description)
        else:
            retPattern.SetDescription(str(description))
            
        retPattern.SetDefault(False)
        retPattern.SetColors(self.__colorList)
        retPattern.SetPwmSequenceDict(self.__pwmSequenceDict)
        return retPattern
    
    def SetName(self,name):
        print "Setting Name: %s"%name
        self.__name = name
    
    def GetName(self):
        return self.__name
    
    def SetDescription(self,description):
        self.__description = description
    
    def GetDescription(self):
        return self.__description
    
    def SetDefault(self,default):
        self.__default = default
        
    def GetDefault(self):
        return self.__default
    
    def SetPwmSequenceDict(self,pwmDict):
        self.__pwmSequenceDict = pwmDict
        
    def GetPwmSequenceDict(self):
        return self.__pwmSequenceDict
        
    def SetColor(self,index,color):
        if index >= len(self.__colorList):
            print "Pattern: BAD INDEX"
            return
        
        self.__colorList[index] = color
        print "New Color list entry is %s for index %d"%(self.__colorList[index], index)
    
    def GetColorByIndex(self,index):
        return self.__colorList[index]
    
    def GetColorList(self):
        return self.__colorList
    
    def SetRequiredColors(self,numColors):
        self.__requiredColors = numColors
        
    def GetRequiredColors(self):
        return self.__requiredColors
            