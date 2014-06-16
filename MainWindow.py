from PyQt4.QtGui import QMainWindow, QWidget, QHBoxLayout, QPushButton, QTabBar, QTabWidget, QVBoxLayout, QMenuBar
from PyQt4.QtCore import Qt
import sys
from PyQt4.QtGui import QApplication
from Tabs import StrobeBrowserTab, StrobeEditTab

class MainWindow(QMainWindow):
    ## __init__ ---------------------------------------------------------
    def __init__(self):
        # Make Main window
        QMainWindow.__init__(self, None)
        self.setWindowTitle("Lightpad")
        self.resize(520, 300);

        # Create main layout for window
        mainWidget = QWidget(self)
        defaultLayout = QVBoxLayout(mainWidget)
        mainWidget.setLayout(defaultLayout)
        
        # Add Menu Bard
        menuBar = self.menuBar()
        menuBar_file = menuBar.addMenu("&File")
        menuBar_edit = menuBar.addMenu("&Edit")
        
        # Add Tabs
        tabWidget = QTabWidget() 
        self.__browserTab = StrobeBrowserTab(QTabWidget)
        self.__editTab = StrobeEditTab(QTabWidget)
         
        print "BOO"
        
        tabWidget.addTab(self.__browserTab, "Stobe Patterns") 
        tabWidget.addTab(self.__editTab, "Edit Strobe Pattern") 
        
        defaultLayout.addWidget(menuBar)
        defaultLayout.addWidget(tabWidget)
        
        # Make the window knwo what is the main widget
        self.setCentralWidget(mainWidget)

        # Make push button
   #     self.__okButton = QPushButton("OKAY");
    #    self.__okButton.clicked.connect(self.__handleDoOkay)
     #   self.__okButton.setMinimumHeight(100)
        
         # Add widget to layout
    #    defaultLayout.addWidget(self.__okButton)       
    def __handleDoOkay(self):
        print "OKAY CLICKED!"