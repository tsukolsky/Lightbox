from util.Enum import Enum

pIndex = Enum(["Name", "Description", "Default", "ColorList","RequiredColors","PWM"])
Colors = Enum(["Red", "Blue", "Green", "Violet", "White"])

DEFAULT_PATTERNS = list()

pattern_zero = list()
pattern_zero.append("Pattern One")
pattern_zero.append( "Pattern One Description")
pattern_zero.append(True)
pattern_zero.append(Colors.Red)
pattern_zero.append(1)
pattern_zero.append([[100,100,1],[150,150,1]])
DEFAULT_PATTERNS.append(pattern_zero)

pattern_one = list()
pattern_one.append("Pattern Two")
pattern_one.append("Pattern Two Description")
pattern_one.append(True)
pattern_one.append(Colors.Red)
pattern_one.append(1)
pattern_one.append([[100,100,1],[150,150,1]])
DEFAULT_PATTERNS.append(pattern_one)

NUM_DEFAULT_PATTERNS = len(DEFAULT_PATTERNS)