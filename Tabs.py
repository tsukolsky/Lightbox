from PyQt4.QtGui import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
import time


def StrobeBrowserTab(QTabWidget):
    def __init__(self):
        print "Making TAB!"
        
        self.browser = QTabWidget(self)
        mainLayout = QVBoxLayout(self)
        
        # Make simple button layout
        row1Layout = QHBoxLayout()
        
        strobeOneButton = QPushButton("Strobe 1")
        strobeTwoButton = QPushButton("Strobe 2")
        strobeThreeButton = QPushButton("Strobe 4")
        
        strobeOneButton.clicked.connect(self.__handleStrobeOneClicked)
        
        row1Layout.addWidget(strobeOneButton)
        row1Layout.addWidget(strobeTwoButton)
        row1Layout.addWidget(strobeThreeButton)
        
        mainLayout.addLayout(row1Layout)
        
        self.browser.setLayout(mainLayout)
        self.show()
    def __handleStrobeOneClicked(self):
        print "StOBE 1"
        
        
        
def StrobeEditTab(QTabWidget):
    def __init__(self):
        print "Tab2"