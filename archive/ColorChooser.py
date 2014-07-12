## This file is outdated, the original idea was  for this to be used when a color should
## be selected, however the popup was a bad idea and this is now DEPRECATED

from PyQt4.QtGui import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt4.QtCore import Qt, SIGNAL

from util.MyPushButton import IDPushButton, TagPushButton
from util.Settings import Colors
from util.event import Event

class ColorChooser(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Color Chooser")
        
        self.__mainLayout = QVBoxLayout()
        
        self.__buttonLayout = QVBoxLayout()
        self.__makeColorButtons()
        
        self.__controlLayout = QHBoxLayout()
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.__cancelClicked)
        
        self.__controlLayout.addStretch(1)
        self.__controlLayout.addWidget(cancelButton)
        
        self.__mainLayout.addLayout(self.__buttonLayout)
        self.__mainLayout.addLayout(self.__controlLayout)
        
        self.setLayout(self.__mainLayout)
        self.__selectedColor = None
        
        self.connect(self, SIGNAL("tagPushButtonClicked(PyQt_PyObject)"), self.__colorClicked)
        
        self.ColorSelected = Event()
        self.CancelSelected = Event()
        
        self.show()
        
    def __makeColorButtons(self):
        numOfColors = len(Colors)
        rowOne = QHBoxLayout()
        for i in range(1,4):
            butt = TagPushButton(self,Colors[i])
            rowOne.addWidget(butt)
        
        rowTwo = QHBoxLayout()
        for i in range(4,7):
            butt = TagPushButton(self,Colors[i])
            rowTwo.addWidget(butt)
        
        rowThree = QHBoxLayout()
        butt = TagPushButton(self,Colors[6])
        rowThree.addWidget(butt)
        rowThree.addStretch(1)
        
        self.__buttonLayout.addLayout(rowOne)
        self.__buttonLayout.addLayout(rowTwo)
        self.__buttonLayout.addLayout(rowThree)
    
    def __colorClicked(self,colorTag):
        print "Color %s clicked"%colorTag
        self.ColorSelected(colorTag)
        self.close()
        
    def __cancelClicked(self):
        print "CANCEL"
        self.CancelSelected()
        self.close()
