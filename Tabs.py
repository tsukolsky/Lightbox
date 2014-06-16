from PyQt4.QtGui import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
import time
from util.event import Event
from util.Log import Log

class StrobeBrowserTab(QWidget):
    def __init__(self):
        print "Making TAB!"
        self.Log = Log()
        QWidget.__init__(self)
        self.__mainLayout = QVBoxLayout(self)
        
        # Make simple button layout
        row1Layout = QHBoxLayout()
        row2Layout = QHBoxLayout()
        row3Layout = QHBoxLayout()
        row4Layout = QHBoxLayout()
        
        ## hate this, disgusting. What happens when we add?
        # Must be generic, event handler
        strobeOneButton = QPushButton("Strobe 1")
        strobeTwoButton = QPushButton("Strobe 2")
        strobeThreeButton = QPushButton("Strobe 3")
        strobeFourButton = QPushButton("Strobe 4")
        strobeFiveButton = QPushButton("Strobe 5")
        strobeSixButton = QPushButton("Strobe 6")
        strobeSevenButton =  QPushButton("Strobe 7")
        strobeEightButton = QPushButton("Strobe 8")
        strobeNineButton = QPushButton("Strobe 9")
        strobeTenButton = QPushButton("Strobe 10")
        strobeElevenButton = QPushButton("Strobe 11")
        strobeTwelveButton = QPushButton("Strobe 12")
        
        strobeOneButton.clicked.connect(self.__handleStrobeOneClicked)
        
        row1Layout.addWidget(strobeOneButton)
        row1Layout.addWidget(strobeTwoButton)
        row1Layout.addWidget(strobeThreeButton)

        row2Layout.addWidget(strobeFourButton)
        row2Layout.addWidget(strobeFiveButton)
        row2Layout.addWidget(strobeSixButton)
        
        row3Layout.addWidget(strobeSevenButton)
        row3Layout.addWidget(strobeEightButton)
        row3Layout.addWidget(strobeNineButton)
        
        row4Layout.addWidget(strobeTenButton)
        row4Layout.addWidget(strobeElevenButton)
        row4Layout.addWidget(strobeTwelveButton)
        
        self.__mainLayout.addLayout(row1Layout)
        self.__mainLayout.addLayout(row2Layout)
        self.__mainLayout.addLayout(row3Layout)
        self.__mainLayout.addLayout(row4Layout)
        
        self.ButtonClicked = Event()
        
        self.ButtonClicked.subscribe(self.__HandleButtonClicked)
        
    def __handleStrobeOneClicked(self):
        print "StOBE 1"
        
    def __HandleButtonClicked(self):
        print "Button Clicked"
        