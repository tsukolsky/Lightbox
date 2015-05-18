from util.Enum import Enum
import platform, os, inspect

RASPI = True
if platform.dist()[0] == "Ubuntu":
    RASPI = False

### Optional Features --------------------------------
ADD_PATTERN_ENABLED = False
PHONE_HOME_ENABLED = False
TIMER_ENABLED = False
MAX_NUM_PRESETS = 16

### Path Settings ------------------------------------
currentFile         = inspect.getfile(inspect.currentframe())
currentPath         = currentFile.split('/util/Settings.py')[0]

PRESET_FILE         = currentPath + "/saved_presets.txt"
START_ICON_LOC      = currentPath + "/icons/Start.png"
STOP_ICON_LOC       = currentPath + "/icons/Stop.png"
SHUTDOWN_ICON_LOC   = currentPath + "/icons/Shutdown.png"
INTENSITY_ICON_LOC  = currentPath + "/icons/Intensity.png"
SAVE_ICON_LOC       = currentPath + "/icons/Save.png"
BACK_ICON_LOC       = currentPath + "/icons/Back.png"
DELETE_ICON_LOC     = currentPath + "/icons/Delete.png"
BLUE_ICON_LOC       = currentPath + "/icons/Blue.png" 
RED_ICON_LOC        = currentPath + "/icons/Red.png"
REDOR_ICON_LOC      = currentPath + "/icons/RedOrange.png"
CYAN_ICON_LOC       = currentPath + "/icons/Cyan.png"
GREEN_ICON_LOC      = currentPath + "/icons/Green.png"
WHITE_ICON_LOC      = currentPath + "/icons/White.png"
YELLOW_ICON_LOC     = currentPath + "/icons/Yellow.png"

#print "Current path is %s. Preset file is %s, Start Icon/Stop icon are %s, %s"%(currentPath, PRESET_FILE, START_ICON_LOC, STOP_ICON_LOC)

### Pi-GPIO Dictionary and WiringPi GPIO Corresponding value ---------------------------
GpioDict = dict()
GpioDict["Red"]         = 7
GpioDict["Red-Orange"]  = 11
GpioDict["Cyan"]        = 12
GpioDict["Green"]       = 13
GpioDict["Blue"]        = 15
GpioDict["White"]       = 16
GpioDict["Yellow"]      = 18

WireGpioDict = dict()
WireGpioDict["Red"]         = 0
WireGpioDict["Red-Orange"]  = 1
WireGpioDict["Cyan"]        = 2
WireGpioDict["Green"]       = 3
WireGpioDict["Blue"]        = 4
WireGpioDict["White"]       = 5
WireGpioDict["Yellow"]      = 6

### Color Declarations -------------------------------
Colors = Enum(["Red", "Red-Orange", "Cyan", "Green", "Blue", "White", "Yellow","Empty"])
ColorsByIndex = ["Red", "Red-Orange", "Cyan", "Green", "Blue", "White", "Yellow","Empty"]

### Pattern Declarations -----------------------------
pIndex = Enum(["Name", "Description", "Default", "ColorList","RequiredColors","PWM", "Id"])

PatternDict = dict()
PatternDict["4Hz"] = 0
PatternDict["4Hz Alternating"] = 1
PatternDict["4Hz Group/Interrupt"] = 2
PatternDict["4Hz Group/Alt"] = 3
PatternDict["6Hz"] = 4
PatternDict["SOS A1-MOD"] = 5
PatternDict["Chirp-Up-Mod"] = 6
PatternDict["Chirp-Up-Mod, 3-Color"] = 7
PatternDict["4Hz 10% Duty"] = 8
PatternDict["4Hz 20% Duty"] = 9
PatternDict["4Hz 30% Duty"] = 10
PatternDict["2Hz Group/Alt"] = 11
PatternDict["Fixed"] = 12
PatternDict["Calibration"] = 13

'''
# These patterns have been DEPRECATED for Release1505. They have been replaced with 4Hz 10/20/30% Duty Interrupt Signals
PatternDict["2Hz 25% Duty"] = 8
PatternDict["2Hz 50% Duty"] = 9
PatternDict["2Hz 2-Color"] = 11
'''


#####################################################################
## Intensity Calibration/Intensity Data
## NOTE* These have been CALIBRATED! DO NOT CHANGE THE NUMBERS UNLESS
## YOU KNOW WHAT YOU ARE DOING!!!
#####################################################################
Intensities = [80,100,200,400,800,1000,1600,2000,3200,4000]

## Individual Color Readings
redIntensityData = dict()
redorIntensityData = dict()
cyanIntensityData = dict()
greenIntensityData = dict()
blueIntensityData = dict()
whiteIntensityData = dict()
yellowIntensityData = dict()

initList = [redIntensityData, redorIntensityData, cyanIntensityData, greenIntensityData, blueIntensityData, whiteIntensityData, yellowIntensityData]
for colorDict in initList:
    colorDict[80]   = 18
    colorDict[100]  = 20
    colorDict[200]  = 25
    colorDict[400]  = 35
    colorDict[800]  = 45
    colorDict[1000] = 62
    colorDict[1600] = 70
    colorDict[2000] = 75
    colorDict[3200] = 90
    colorDict[4000] = 95
    
################################################################
## Edits to the intensities during testing: EDIT HERE
################################################################
redIntensityData[80] = 2
redIntensityData[100] = 3
redIntensityData[200] = 4
redIntensityData[400] = 7
redIntensityData[800] = 13
redIntensityData[1000] = 16
redIntensityData[1600] = 25
redIntensityData[2000] = 33
redIntensityData[3200] = 52
redIntensityData[4000] = 72

redorIntensityData[80] = 2
redorIntensityData[100] = 3
redorIntensityData[200] = 4
redorIntensityData[400] = 8
redorIntensityData[800] = 14
redorIntensityData[1000] = 17
redorIntensityData[1600] = 27
redorIntensityData[2000] = 33
redorIntensityData[3200] = 52
redorIntensityData[4000] = 72

cyanIntensityData[80] = 2
cyanIntensityData[100] = 4
cyanIntensityData[200] = 7
cyanIntensityData[400] = 12
cyanIntensityData[800] = 22
cyanIntensityData[1000] = 27
cyanIntensityData[1600] = 41
cyanIntensityData[2000] = 52
cyanIntensityData[3200] = 78
cyanIntensityData[4000] = 100

greenIntensityData[80] = 2
greenIntensityData[100] = 3
greenIntensityData[200] = 5
greenIntensityData[400] = 9
greenIntensityData[800] = 16
greenIntensityData[1000] = 20
greenIntensityData[1600] = 32
greenIntensityData[2000] = 40
greenIntensityData[3200] = 65
greenIntensityData[4000] = 80

blueIntensityData[80] = 3
blueIntensityData[100] = 4
blueIntensityData[200] = 6
blueIntensityData[400] = 10
blueIntensityData[800] = 19
blueIntensityData[1000] = 25
blueIntensityData[1600] = 36
blueIntensityData[2000] = 44
blueIntensityData[3200] = 69
blueIntensityData[4000] = 85

whiteIntensityData[80] = 2
whiteIntensityData[100] = 2
whiteIntensityData[200] = 3
whiteIntensityData[400] = 6
whiteIntensityData[800] = 11
whiteIntensityData[1000] = 15
whiteIntensityData[1600] = 22
whiteIntensityData[2000] = 28
whiteIntensityData[3200] = 44
whiteIntensityData[4000] = 58

yellowIntensityData[80] = 2
yellowIntensityData[100] = 3
yellowIntensityData[200] = 4
yellowIntensityData[400] = 6
yellowIntensityData[800] = 13
yellowIntensityData[1000] = 15
yellowIntensityData[1600] = 27
yellowIntensityData[2000] = 38
yellowIntensityData[3200] = 100
yellowIntensityData[4000] = 100

## All the dictionaries put into one main for qucker access-- do not edit
IntensityDict = dict()
IntensityDict[ColorsByIndex[Colors.Red]] = redIntensityData
IntensityDict["Red-Orange"] = redorIntensityData
IntensityDict[ColorsByIndex[Colors.Cyan]] = cyanIntensityData
IntensityDict[ColorsByIndex[Colors.Green]] = greenIntensityData
IntensityDict[ColorsByIndex[Colors.Blue]] = blueIntensityData
IntensityDict[ColorsByIndex[Colors.White]] = whiteIntensityData
IntensityDict[ColorsByIndex[Colors.Yellow]] = yellowIntensityData

#################################################################
## Default Patterns
#################################################################

DEFAULT_PATTERNS = list()

pattern_zero = list()
pattern_zero.append("4Hz")
pattern_zero.append("Continuous 4Hz 50% Duty")
pattern_zero.append(True)
pattern_zero.append([ColorsByIndex[Colors.Empty]])
pattern_zero.append(1)
tmpDict = dict()
tmpDict[0] = [(.125,.125)]    # tuple
pattern_zero.append(tmpDict)
pattern_zero.append(0)
DEFAULT_PATTERNS.append(pattern_zero)

pattern_one = list()
pattern_one.append("4Hz Alternating")
pattern_one.append("2-Color, 4Hz, 1-1 Alternating")
pattern_one.append(True)
pattern_one.append([ColorsByIndex[Colors.Empty], ColorsByIndex[Colors.Empty]])
pattern_one.append(2)
tmpDict = dict()
tmpDict[0] = [(.125, .125)]
tmpDict[1] = [(.125, .125)]
pattern_one.append(tmpDict)
pattern_one.append(1)
DEFAULT_PATTERNS.append(pattern_one)

pattern_two = list()
pattern_two.append("4Hz Group/Interrupt")
pattern_two.append("4Hz, 4-3 Interrupt")
pattern_two.append(True)
pattern_two.append([ColorsByIndex[Colors.Empty]])
pattern_two.append(1)
tmpDict = dict()
tmpDict[0] = [(.125, .125), (.125, .125), (.125, .125), (.125, .250), (.125, .125), (.125, .125), (.125, .250)]
pattern_two.append(tmpDict)
pattern_two.append(2)
DEFAULT_PATTERNS.append(pattern_two)

pattern_oops = list()
pattern_oops.append("4Hz Group/Alt")
pattern_oops.append("4Hz, 4-3 Alternating")
pattern_oops.append(True)
pattern_oops.append([ColorsByIndex[Colors.Empty], ColorsByIndex[Colors.Empty]])
pattern_oops.append(2)
tmpDict = dict()
tmpDict[0] = [(.125, .125), (.125, .125), (.125, .125), (.125, .250)]
tmpDict[1] = [(.125, .125), (.125, .125), (.125, .250)]
pattern_oops.append(tmpDict)
pattern_oops.append(3)
DEFAULT_PATTERNS.append(pattern_oops)

pattern_three = list()
pattern_three.append("6Hz")
pattern_three.append("Continuous 6Hz")
pattern_three.append(True)
pattern_three.append([ColorsByIndex[Colors.Empty]])
pattern_three.append(1)
tmpDict = dict()
tmpDict[0] = [(.083, .083)]
pattern_three.append(tmpDict)
pattern_three.append(4)
DEFAULT_PATTERNS.append(pattern_three)

pattern_four = list()
pattern_four.append("SOS A1-MOD")
pattern_four.append("SOS-A1")
pattern_four.append(True)
pattern_four.append([ColorsByIndex[Colors.Empty]])
pattern_four.append(1)
tmpDict = dict()
tmpDict[0] = [(.125, .125), (.125, .125), (.125, .125), (.375, .125), (.375, .125), (.375, .125), (.125, .125), (.125, .125), (.125, .300)]
pattern_four.append(tmpDict)
pattern_four.append(5)
DEFAULT_PATTERNS.append(pattern_four)

pattern_five = list()
pattern_five.append("Chirp-Up-Mod")
pattern_five.append("2Hz/5, 4Hz/8, 6Hz/15")
pattern_five.append(True)
pattern_five.append([ColorsByIndex[Colors.Empty]])
pattern_five.append(1)
tmpDict = dict()
tmpDict[0] = [(.25, .25), (.25, .25), (.25, .25), (.25, .25), (.25, .25), \
              (.125, .125), (.125, .125), (.125, .125), (.125, .125), (.125, .125), (.125, .125), (.125, .125), (.125, .125), \
              (.083, .083), (.083, .083), (.083, .083), (.083, .083), (.083, .083), (.083, .083), (.083, .083), \
              (.083, .083), (.083, .083), (.083, .083), (.083, .083), (.083, .083), (.083, .083), (.083, .083), \
              (.083, .083)]
pattern_five.append(tmpDict)
pattern_five.append(6)
DEFAULT_PATTERNS.append(pattern_five)

pattern_six = list()
pattern_six.append("Chirp-Up-Mod, 3-Color")
pattern_six.append("A:2Hz/5, B: 4Hz/8, C: 6Hz/15")
pattern_six.append(True)
pattern_six.append([ColorsByIndex[Colors.Empty],ColorsByIndex[Colors.Empty], ColorsByIndex[Colors.Empty]])
pattern_six.append(3)
tmpDict = dict()
tmpDict[0] = [(.25, .25), (.25, .25), (.25, .25), (.25, .25), (.25, .25)]
tmpDict[1] = [(.125, .125), (.125, .125), (.125, .125), (.125, .125), (.125, .125), (.125, .125), (.125, .125), (.125, .125)]
tmpDict[2] = [(.083, .083), (.083, .083), (.083, .083), (.083, .083), (.083, .083), (.083, .083), (.083, .083), \
              (.083, .083), (.083, .083), (.083, .083), (.083, .083), (.083, .083), (.083, .083), (.083, .083), \
              (.083, .083)]
pattern_six.append(tmpDict)
pattern_six.append(7)
DEFAULT_PATTERNS.append(pattern_six)

pattern_seven = list()
pattern_seven.append("4Hz 10% Duty")
pattern_seven.append("4Hz Interrupt, 10% Duty, 4-3 Alt")
pattern_seven.append(True)
pattern_seven.append([ColorsByIndex[Colors.Empty], ColorsByIndex[Colors.Empty]])
pattern_seven.append(2)
tmpDict = dict()
pattern_seven.append(8)
DEFAULT_PATTERNS.append(pattern_seven)

pattern_eight = list()
pattern_eight.append("4Hz 20% Duty")
pattern_eight.append("4Hz Continuous, 20% Duty, 4-3 Alt")
pattern_eight.append(True)
pattern_eight.append([ColorsByIndex[Colors.Empty], ColorsByIndex[Colors.Empty]])
pattern_eight.append(2)
tmpDict = dict()
pattern_eight.append(tmpDict)
pattern_eight.append(9)
DEFAULT_PATTERNS.append(pattern_eight)

pattern_nine = list()
pattern_nine.append("4Hz 30% Duty")
pattern_nine.append("4Hz Continuous, 30% Duty, 4-3 Alt")
pattern_nine.append(True)
pattern_nine.append([ColorsByIndex[Colors.Empty], ColorsByIndex[Colors.Empty]])
pattern_nine.append(2)
tmpDict = dict()
pattern_nine.append(tmpDict)
pattern_nine.append(10)
DEFAULT_PATTERNS.append(pattern_nine)

pattern_ten = list()
pattern_ten.append("2Hz Group/Alt")
pattern_ten.append("2-Color, 2Hz 25% duty cycle, 4-3 Alt")
pattern_ten.append(True)
pattern_ten.append([ColorsByIndex[Colors.Empty],ColorsByIndex[Colors.Empty]])
pattern_ten.append(2)
tmpDict = dict()
pattern_ten.append(tmpDict)
pattern_ten.append(11)
DEFAULT_PATTERNS.append(pattern_ten)


pattern_eleven = list()
pattern_eleven.append("Fixed")
pattern_eleven.append("Continuous Signal")
pattern_eleven.append(True)
pattern_eleven.append([ColorsByIndex[Colors.Empty]])
pattern_eleven.append(1)
tmpDict = dict()
tmpDict[0] = [(1.0, 0)]
pattern_eleven.append(tmpDict)
pattern_eleven.append(12)
DEFAULT_PATTERNS.append(pattern_eleven)

'''
THESE PATTERNS ARE NOW DEPRECATED

pattern_seven = list()
pattern_seven.append("2Hz 25% Duty")
pattern_seven.append("2Hz Continuous, 25% Duty")
pattern_seven.append(True)
pattern_seven.append([ColorsByIndex[Colors.Empty]])
pattern_seven.append(1)
tmpDict = dict()
tmpDict[0] = [(.125, .375)]
pattern_seven.append(tmpDict)
pattern_seven.append(8)
DEFAULT_PATTERNS.append(pattern_seven)

pattern_eight = list()
pattern_eight.append("2Hz 50% Duty")
pattern_eight.append("2Hz Continuous, 50% Duty")
pattern_eight.append(True)
pattern_eight.append([ColorsByIndex[Colors.Empty]])
pattern_eight.append(1)
tmpDict = dict()
tmpDict[0] = [(.250, .250)]
pattern_eight.append(tmpDict)
pattern_eight.append(9)
DEFAULT_PATTERNS.append(pattern_eight)



pattern_ten = list()
pattern_ten.append("2Hz 2-Color")
pattern_ten.append("2-Color, 2Hz 50% Duty")
pattern_ten.append(True)
pattern_ten.append([ColorsByIndex[Colors.Empty], ColorsByIndex[Colors.Empty]])
pattern_ten.append(2)
tmpDict = dict()
tmpDict[0] = [(.250, .250), (.250, .250), (.250, .250), (.250, .250)]
tmpDict[1] = tmpDict[0]
pattern_ten.append(tmpDict)
pattern_ten.append(11)
DEFAULT_PATTERNS.append(pattern_ten)
'''

'''
pattern_calibration = list()
pattern_calibration.append("Calibration")
pattern_calibration.append("350ms/1650ms")
pattern_calibration.append(True)
pattern_calibration.append([ColorsByIndex[Colors.Empty]])
pattern_calibration.append(1)
tmpDict = dict()
tmpDict[0] = [(.350, 1.650)]
pattern_calibration.append(tmpDict)
pattern_calibration.append(13)
DEFAULT_PATTERNS.append(pattern_calibration)
'''

NUM_DEFAULT_PATTERNS = len(DEFAULT_PATTERNS)
