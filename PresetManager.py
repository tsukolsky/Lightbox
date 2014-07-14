import os, time
from Pattern import Pattern
from util.Settings import  DEFAULT_PATTERNS, pIndex, Colors, ColorsByIndex
RASPI = True
PRESET_FILE = None
if RASPI:
    PRESET_FILE = "/home/pi/Desktop/Lightbox/saved_presets.txt"
else:
    PRESET_FILE = "/home/todd/workspace/LightPad/saved_presets.txt"

class PresetManager():
    def __init__(self, log = None):
        self.log = log
        self.CALLING_CLASS = "PresetManager"

    def __log(self, message):
        if self.log != None:
            self.log.LOG(self.CALLING_CLASS, message)
            
    def GetPresetPatterns(self):
        self.__log("Get Preset Pattern")
        retList = list()
        try:
            if self.__fileExists():
                fh = open(PRESET_FILE, 'r')
                lines = fh.readlines()
                self.__log("Got %d lines from file"%len(lines))
                findingPresets = True
                currentLine = 0
                while findingPresets and (currentLine + 2) < len(lines):
                    if lines[currentLine].rstrip() == "--":
                        # new entry
                        currentLine += 1
                        name = lines[currentLine].rstrip()
                        currentLine += 1
                        colors = lines[currentLine].rstrip().split(',')
                        self.__log("Name: %s, Colors: %s"%(name, colors))
                        for defaultPattern in DEFAULT_PATTERNS:
                            if defaultPattern[0] == name:
                                name = defaultPattern[pIndex.Name]
                                des = defaultPattern[pIndex.Description] 
                                default = defaultPattern[pIndex.Default]
                                reqColors = defaultPattern[pIndex.RequiredColors]
                                pwm = defaultPattern[pIndex.PWM]
                                tmpPattern = Pattern(name, des, default, colors, reqColors, pwm, self.log) 
                                retList += [tmpPattern]
                        currentLine += 1
                        self.__log("Current line now %d"%currentLine)
                    else:
                        currentLine += 1
                fh.close()
        except:
            os.system("rm %s"%PRESET_FILE)
            self.__log("Presets have been deleted, corrupted file")
            retList = list()
            
        return retList
        
    def SavePresetPattern(self,presetPattern):
        self.__log("Saving pattern")
        retBool = True
        fh = None
        if (self.__fileExists()):
            fh = open(PRESET_FILE, 'a')
        else:
            fh = open(PRESET_FILE, 'w')
            
        linesToWrite = list()
        linesToWrite.append("--\n")
        linesToWrite.append(presetPattern.GetName()+"\n")
        linesToWrite.append(",".join(presetPattern.GetColorList())+"\n")
        fh.writelines(linesToWrite)
        fh.close()
        
    def DeletePresetPattern(self,presetPattern):
        self.__log("Delete preset pattern")
        retBool = True
        if self.__fileExists():
            fh = open(PRESET_FILE, 'r')
            lines = fh.readlines()
            self.__log("Read %d lines"%len(lines))
            for ind,line in enumerate(lines):
                if line.rstrip() == presetPattern.GetName():
                    self.__log("Name match found")
                    if lines[ind+1].rstrip() == ",".join(presetPattern.GetColorList()) and lines[ind-1] == "--\n":
                        self.__log("Color match found")
                        fh.close()
                        newFh = open(PRESET_FILE,'w')
                        for i in range(0,ind-1):
                            newFh.write(lines[i])
                        for j in range(ind+2,len(lines)):
                            newFh.write(lines[j])
                        newFh.close()
                        break
            try:
                fh.close()                     
            except:
                self.__log("File closed")
    def __fileExists(self):
        if os.path.exists(PRESET_FILE):
            return True
        else:
            self.__log("File doesn't exist, nothign to get")
            return False