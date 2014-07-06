from PyQt4.QtGui import QPushButton 
from PyQt4.QtCore import pyqtSlot, SIGNAL, SLOT

class TagPushButton(QPushButton):
    def __init__(self,parentWidget,elementID):
        super(TagPushButton, self).__init__(elementID)
        self.__elementID = elementID
        self.__parent = parentWidget
        self.connect(self, SIGNAL('clicked()'), self, SLOT("triggerOutput()"))
        
    @pyqtSlot()
    def triggerOutput(self):
        #print "MyPushButton triggered"
        self.__parent.emit(SIGNAL("tagPushButtonClicked(PyQt_PyObject)"), self.__elementID)
        
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