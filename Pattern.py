import os, sys, time
#from RPGPIO import PWM

class Pattern():
    def __init__(self, name = "", des = "", default = False, colorList = list(), numRequired = -1, pwm = list()):
        self.__name = name
        self.__description = des
        self.__default = default
        self.__colorList = colorList
        self.__requiredColors = numRequired
        self.__pwmSequence = pwm
        
    def CopyPattern(self,name = None, description = None):
        retPattern = Pattern()
        print description
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
        retPattern.SetPwmSequence(self.__pwmSequence)
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
    
    def SetColors(self,colorList):
        self.__colorList = colorList
        
    #def SetColors(self,colorOne = None, colorTwo = None, colorThree = None):
    #    tmpColors = list()
    #    if colorOne is not None:
    #        tmpColors = [colorOne]
    #    if colorTwo is not None:
    ##    if colorThree is not None:
     #       tmpColors += [colorThree]
     #   
     #   if len(tmpColors) != 0:
     #       self.SetColors(tmpColors)
    
    def GetColors(self):
        return self.__colorList
    
    def SetRequiredColors(self,numColors):
        self.__requiredColors = numColors
        
    def GetRequiredColors(self):
        return self.__requiredColors
                
    def SetPwmSequence(self,sequence):
        self.__pwmSequence = sequence
        
    def GetPwm(self):
        return self.__pwmSequence
            