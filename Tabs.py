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
        
        self.__buttonLayout = QVBoxLayout()
        for x in range(0,12):
            self.AddButton(False)
            
        self.__redrawLayout()    
        #self.ButtonClicked = Event()
        #self.ButtonClicked.subscribe(self.__HandleButtonClicked)
     
    def __Log(self,message):
        self.__log.LOG(self.__logTitle,message)
           
    def __handleStrobeOneClicked(self):
        print "StOBE 1"
        
    def __HandleButtonClicked(self):
        print "Button Clicked"
        
    def AddButton(self, redrawLayout = False):
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
    
    def __clearLayout(self, layout):
        if layout is not None:
            print type(layout)
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.hide()
                else:
                    self.__clearLayout(item.layout())
            
    def __redrawLayout(self):
        self.__clearLayout(self.__buttonLayout)
        self.__buttonLayout = QVBoxLayout()
        self.__Log("Redrawing Buttons")
        numOfButtons = len(self.__patternPresets)
        numOfRows = numOfButtons/BUTTONS_PER_ROW
        if numOfButtons%BUTTONS_PER_ROW != 0:
            numOfRows += 1
            
        print numOfButtons,numOfRows
        
        for i in range(0,numOfRows):
            print "New Row"
            newRow = QHBoxLayout()
            buttonsLeft = numOfButtons - i*BUTTONS_PER_ROW
            buttonsInRow = BUTTONS_PER_ROW
            if buttonsLeft < BUTTONS_PER_ROW:
                buttonsInRow = buttonsLeft
            for j in range(0,buttonsInRow):
                print "Adding Widget"
                newRow.addWidget(self.__patternPresets[i*BUTTONS_PER_ROW+j][1])
            print "Adding Row"
            self.__buttonLayout.addLayout(newRow)
        
        self.__mainLayout.addLayout(self.__buttonLayout)  
            
        
    def __patternPressed(self,buttonTag):
        self.__Log("Pattern \'%s\' pressed"%buttonTag)
        self.__selectedPattern = buttonTag
        
        
        
        
        
        
        
        
        
        