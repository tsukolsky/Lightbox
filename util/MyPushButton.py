from PyQt4.QtGui import QPushButton 
from PyQt4.QtCore import pyqtSlot, SIGNAL, SLOT

class TagPushButton(QPushButton):
    def __init__(self,parentWidget,tag):
        super(TagPushButton, self).__init__(tag)
        self.__tag = tag
        self.__parent = parentWidget
        self.connect(self, SIGNAL('clicked()'), self, SLOT("triggerOutput()"))
        
    @pyqtSlot()
    def triggerOutput(self):
        #print "MyPushButton triggered"
        self.__parent.emit(SIGNAL("tagPushButtonClicked(PyQt_PyObject)"), self.__tag)
        
class IDPushButton(QPushButton):
    def __init__(self,parentWidget,inputText,elementID):
        super(IDPushButton, self).__init__(inputText)
        self.__elementID = elementID
        self.__parent = parentWidget
        self.connect(self, SIGNAL('clicked()'), self, SLOT("triggerOutput()"))
        
    @pyqtSlot()
    def triggerOutput(self):
        #print "MyPushButton triggered"
        self.__parent.emit(SIGNAL("idPushButtonClicked(PyQt_PyObject)"), self.__elementID)
        
class DurationPushButton(QPushButton):
    def __init__(self, parentWidget, durationTag):
        super(DurationPushButton, self).__init__(durationTag)
        self.__tag = durationTag
        self.__parent = parentWidget
        self.connect(self, SIGNAL('clicked()'), self, SLOT("triggerOutput()"))
        
    @pyqtSlot()
    def triggerOutput(self):
        self.__parent.emit(SIGNAL("durationPushButtonClicked(PyQt_PyObject)"), self.__tag)
        