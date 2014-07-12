from util.Enum import Enum

pIndex = Enum(["Name", "Description", "Default", "ColorList","RequiredColors","PWM"])
Colors = Enum(["Red", "Red-Orange", "Cyan", "Green", "Blue", "White", "Yellow","Empty"])
ColorsByIndex = ["Red", "Red-Orange", "Cyan", "Green", "Blue", "White", "Yellow","Empty"]

GpioDict = dict()
GpioDict["Red"]         = 7
GpioDict["Red-Orange"]  = 11
GpioDict["Cyan"]        = 12
GpioDict["Green"]       = 13
GpioDict["Blue"]        = 15
GpioDict["White"]       = 16
GpioDict["Yellow"]      = 18

IntensityDict = dict()
IntensityDict[0] = 0.0
IntensityDict[400] = 10.0
IntensityDict[800] = 20.0
IntensityDict[1200] = 30.0
IntensityDict[1600] = 40.0
IntensityDict[2000] = 50.0
IntensityDict[2400] = 60.0
IntensityDict[2800] = 70.0
IntensityDict[3200] = 80.0
IntensityDict[3600] = 90.0
IntensityDict[4000] = 100.0

DEFAULT_PATTERNS = list()

# Color List MUST be initialized
CONTINOUS_PATTERN = -1

pattern_zero = list()
pattern_zero.append("4Hz")
pattern_zero.append("Continuous 4Hz")
pattern_zero.append(True)
pattern_zero.append([ColorsByIndex[Colors.Empty]])
pattern_zero.append(1)
tmpDict = dict()
tmpDict[0] = [4,CONTINOUS_PATTERN, 0]
pattern_zero.append(tmpDict)
DEFAULT_PATTERNS.append(pattern_zero)

pattern_one = list()
pattern_one.append("4Hz Alternating")
pattern_one.append("2-Color, 4Hz, 1-1 Alternating")
pattern_one.append(True)
pattern_one.append([ColorsByIndex[Colors.Empty], ColorsByIndex[Colors.Empty]])
pattern_one.append(2)
tmpDict = dict()
tmpDict[0] = [4,0.25, 0]
tmpDict[1] = [4,0.25, 0]
pattern_one.append(tmpDict)
DEFAULT_PATTERNS.append(pattern_one)

pattern_two = list()
pattern_two.append("4Hz Group/Interrupt")
pattern_two.append("4Hz, 4-3 Interrupt")
pattern_two.append(True)
pattern_two.append([ColorsByIndex[Colors.Empty]])
pattern_two.append(1)
tmpDict = dict()
tmpDict[0] = [4, 1.0, 0.125]
tmpDict[1] = [4, .75, 0.125] 
pattern_two.append(tmpDict)
DEFAULT_PATTERNS.append(pattern_two)

pattern_oops = list()
pattern_oops.append("4Hz Group/Alt")
pattern_oops.append("4Hz, 4-3 Alternating")
pattern_oops.append(True)
pattern_oops.append([ColorsByIndex[Colors.Empty], ColorsByIndex[Colors.Empty]])
pattern_oops.append(2)
tmpDict = dict()
tmpDict[0] = [4, 1.0, 0.125]
tmpDict[1] = [4, .75, 0.125] 
pattern_oops.append(tmpDict)
DEFAULT_PATTERNS.append(pattern_oops)

pattern_three = list()
pattern_three.append("6Hz")
pattern_three.append("Continuous 6Hz")
pattern_three.append(True)
pattern_three.append([ColorsByIndex[Colors.Empty]])
pattern_three.append(1)
tmpDict = dict()
tmpDict[0] = [6, CONTINOUS_PATTERN, 0]
pattern_three.append(tmpDict)
DEFAULT_PATTERNS.append(pattern_three)

pattern_four = list()
pattern_four.append("SOS A1-MOD")
pattern_four.append("SOS-A1")
pattern_four.append(True)
pattern_four.append([ColorsByIndex[Colors.Empty]])
pattern_four.append(1)
tmpDict = dict()
tmpDict[0] = [4, .75, 0]
tmpDict[1] = [2.6, .375, .125]
tmpDict[2] = tmpDict[1]
tmpDict[3] = tmpDict[1]
tmpDict[4] = tmpDict[0]
pattern_four.append(tmpDict)
DEFAULT_PATTERNS.append(pattern_four)

pattern_five = list()
pattern_five.append("Chirp-Up-Mod")
pattern_five.append("2Hz/5, 4Hz/8, 6Hz/15")
pattern_five.append(True)
pattern_five.append([ColorsByIndex[Colors.Empty]])
pattern_five.append(1)
tmpDict = dict()
tmpDict[0] = [2, 2.5, 0]
tmpDict[1] = [4, 2, 0]
tmpDict[2] = [6, 2.5, 0]
pattern_five.append(tmpDict)
DEFAULT_PATTERNS.append(pattern_five)

pattern_six = list()
pattern_six.append("Chirp-Up-Mod, 3-Color")
pattern_six.append("A:2Hz/5, B: 4Hz/8, C: 6Hz/15")
pattern_six.append(True)
pattern_six.append([ColorsByIndex[Colors.Empty],ColorsByIndex[Colors.Empty], ColorsByIndex[Colors.Empty]])
pattern_six.append(3)
tmpDict = dict()
tmpDict[0] = [2, 2.5, 0]
tmpDict[1] = [4, 2, 0]
tmpDict[2] = [6, 2.5, 0]
pattern_six.append(tmpDict)
DEFAULT_PATTERNS.append(pattern_six)

pattern_seven = list()
pattern_seven.append("2Hz 25% Duty")
pattern_seven.append("2Hz Continuous, 25% Duty")
pattern_seven.append(True)
pattern_seven.append([ColorsByIndex[Colors.Empty]])
pattern_seven.append(1)
tmpDict = dict()
tmpDict[0] = [4, .125, .250] # Jerry Rigged 25% duty cycle
pattern_seven.append(tmpDict)
DEFAULT_PATTERNS.append(pattern_seven)

pattern_eight = list()
pattern_eight.append("2Hz 50% Duty")
pattern_eight.append("2Hz Continuous, 50% Duty")
pattern_eight.append(True)
pattern_eight.append([ColorsByIndex[Colors.Empty]])
pattern_eight.append(1)
tmpDict = dict()
tmpDict[0] = [2, CONTINOUS_PATTERN, 0]
pattern_eight.append(tmpDict)
DEFAULT_PATTERNS.append(pattern_eight)

pattern_nine = list()
pattern_nine.append("2Hz Group/Alt")
pattern_nine.append("2-Color, 2Hz 25% duty cycle, 4-3 Alt")
pattern_nine.append(True)
pattern_nine.append([ColorsByIndex[Colors.Empty],ColorsByIndex[Colors.Empty]])
pattern_nine.append(2)
tmpDict = dict()                    ## Don't know how to fool this one.
pattern_nine.append(tmpDict)
DEFAULT_PATTERNS.append(pattern_nine)

pattern_ten = list()
pattern_ten.append("2Hz 2-Color")
pattern_ten.append("2-Color, 2Hz 50% Duty")
pattern_ten.append(True)
pattern_ten.append([ColorsByIndex[Colors.Empty], ColorsByIndex[Colors.Empty]])
pattern_ten.append(2)
tmpDict = dict()
tmpDict[0] = [2, 2, 0]
tmpDict[1] = [2, 2, 0]
pattern_ten.append(tmpDict)
DEFAULT_PATTERNS.append(pattern_ten)

pattern_eleven = list()
pattern_eleven.append("Fixed")
pattern_eleven.append("Continous Signal")
pattern_eleven.append(True)
pattern_eleven.append([ColorsByIndex[Colors.Empty]])
pattern_eleven.append(1)
tmpDict = [200, CONTINOUS_PATTERN, 0]
pattern_eleven.append(tmpDict)
DEFAULT_PATTERNS.append(pattern_eleven)

NUM_DEFAULT_PATTERNS = len(DEFAULT_PATTERNS)