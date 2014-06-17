from PyQt4.QtGui import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QIcon, QFont
import time
from util.event import Event
from util.Log import Log

BUTTONS_PER_ROW = 4
MIN_BUTTON_HEIGHT = 100
MIN_BUTTON_WIDTH = 100

class StrobeBrowserTab(QWidget):
    def __init__(self, log):
        self.__log = log
        self.__logTitle = "StrobeBrowserTab"
        
        QWidget.__init__(self)
        self.__mainLayout = QVBoxLayout(self)

        # Patterns        
        self.__patternPresets = list() 
        self.__patternLayouts = list()
        
        for x in range(0,12):
            self.__addButton(False)
            
        self.__redrawLayout()    
        #self.ButtonClicked = Event()
        #self.ButtonClicked.subscribe(self.__HandleButtonClicked)
     
    def __Log(self,message):
        self.__log.LOG(self.__logTitle,message)
           
    def __handleStrobeOneClicked(self):
        print "StOBE 1"
        
    def __HandleButtonClicked(self):
        print "Button Clicked"
        
    def __addButton(self, redrawLayout = False):
        buttonNumber = len(self.__patternPresets) + 1
        print "New button, already have %d"%buttonNumber
        buttonTag = "Pattern %d"%buttonNumber
        newButton = QPushButton(buttonTag)
        newButton.setMinimumSize(MIN_BUTTON_WIDTH,MIN_BUTTON_HEIGHT)
        font = QFont(newButton.font())
        font.setPointSize(24)
        newButton.setFont(font)
        newButton.clicked.connect(lambda: self.__patternPressed(buttonTag))
        temp = [buttonTag, newButton]
        self.__patternPresets.append(temp)
        if redrawLayout:
            self.__redrawLayout()
        
    def __redrawLayout(self):
        self.__Log("Redrawing Buttons")
        numOfButtons = len(self.__patternPresets)
        numOfRows = numOfButtons/BUTTONS_PER_ROW
        print numOfRows
        for i in range(0,numOfRows):
            newRow = QHBoxLayout()
            for j in range(0,BUTTONS_PER_ROW):
                newRow.addWidget(self.__patternPresets[i*BUTTONS_PER_ROW+j][1])
            self.__patternLayouts += [newRow]
            self.__mainLayout.addLayout(newRow)    
            
        
    def __patternPressed(self,buttonTag):
        self.__Log("Pattern \'%s\' pressed"%buttonTag)
        self.__selectedPattern = buttonTag
        
        
        
        
        
        
        
        
        
        