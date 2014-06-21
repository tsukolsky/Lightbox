from PyQt4.QtGui import QPushButton 
from PyQt4.QtCore import pyqtSlot, SIGNAL, SLOT

class MyPushButton(QPushButton):
    def __init__(self,parentWidget,elementID):
        super(MyPushButton, self).__init__(elementID)
        self.__elementID = elementID
        self.__parent = parentWidget
        self.connect(self, SIGNAL('clicked()'), self, SLOT("triggerOutput()"))
        
    @pyqtSlot()
    def triggerOutput(self):
        #print "MyPushButton triggered"
        self.__parent.emit(SIGNAL("buttonXClicked(PyQt_PyObject)"), self.__elementID)
        