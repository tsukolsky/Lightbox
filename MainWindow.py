from PyQt4.QtGui import QMainWindow, QWidget, QHBoxLayout, QPushButton, QTabBar, QTabWidget, QVBoxLayout, QMenuBar, QAction
from PyQt4.QtCore import Qt
import sys
from PyQt4.QtGui import QApplication
from Tabs import StrobeBrowserTab

class MainWindow(QMainWindow):
    FILE_MENU = "&File"
    EXIT_MENU = "E&xit"
    
    ## __init__ ---------------------------------------------------------
    def __init__(self):
        # Make Main window
        QMainWindow.__init__(self, None)
        self.setWindowTitle("Lightbox")
        self.resize(520, 300);

        # Create main layout for window
        mainWidget = QWidget(self)
        mainLayout = QVBoxLayout(mainWidget)
        mainWidget.setLayout(mainLayout)
        
        # Add Menu Bard
        self.__menu = self.__createMenu()
        
        # Add Tabs
        self.__tabs = QTabWidget()
        self.__BrowserTab = StrobeBrowserTab() 
        self.__tabs.addTab(self.__BrowserTab, "Stobe Patterns")  
        mainLayout.addWidget(self.__tabs)
        
        # Make the window knwo what is the main widget
        self.setCentralWidget(mainWidget)

    def __createMenu(self):
        menu = self.menuBar()
        
        fileMenu = menu.addMenu(MainWindow.FILE_MENU)
        
        exitAction = QAction(menu)
        exitAction.setText(MainWindow.EXIT_MENU)
        exitAction.triggered.connect(self.__exit)
        fileMenu.addAction(exitAction)
        
    def __exit(self):
        self.close()
        