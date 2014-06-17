from PyQt4.QtGui import QMainWindow, QWidget, QHBoxLayout, QPushButton, QTabBar, \
                        QTabWidget, QVBoxLayout, QMenuBar, QAction, QIcon, QLabel, QFont
from PyQt4.QtCore import Qt
import sys
from PyQt4.QtGui import QApplication
from Tabs import StrobeBrowserTab
from util.Log import Log

MIN_BUTTON_HEIGHT = 100
MIN_BUTTON_WIDTH = 100

class MainWindow(QMainWindow):
    FILE_MENU = "&File"
    EXIT_MENU = "E&xit"
    
    ## __init__ ---------------------------------------------------------
    def __init__(self, Log = None):
        # Make Main window
        QMainWindow.__init__(self, None)
        self.setWindowTitle("Lightbox")
        self.resize(800, 480)       # Screen Size
        self.__log = Log
        self.__logTitle = "MainWindow"
        if self.__log == None:
            print "No Log File"
            self.close()
            
        # Create main layout for window
        mainWidget = QWidget(self)
        mainLayout = QVBoxLayout(mainWidget)
        mainWidget.setLayout(mainLayout)
      
        # Add Menu Bard
        self.__menu = self.__createMenu()
        
        # Add Tabs
        self.__tabs = QTabWidget()
        self.__BrowserTab = StrobeBrowserTab(self.__log) 
        self.__tabs.addTab(self.__BrowserTab, "Stobe Patterns")  
        
        ## Toolbar that is always there->Selected Pattern, Start, Stop, Current State Label
        self.__currentPatternLabel = QLabel("No Pattern Selected")
        font = self.__currentPatternLabel.font()
        font.setPointSize(24)
        self.__currentPatternLabel.setFont(font)
        self.StartButton = QPushButton("Start")
        font = self.StartButton.font()
        font.setPointSize(24)
        self.StartButton.setFont(font)
        self.StartButton.setMinimumSize(MIN_BUTTON_WIDTH, MIN_BUTTON_HEIGHT)
        startIcon = QIcon("icons/Start.png")
        stopIcon = QIcon("icons/Stop.png")
        self.StartButton.setIcon(startIcon)
        self.StopButton = QPushButton("Stop")
        font = self.StopButton.font()
        font.setPointSize(24)
        self.StopButton.setFont(font)
        self.StopButton.setIcon(stopIcon)
        self.StopButton.setMinimumSize(MIN_BUTTON_WIDTH, MIN_BUTTON_HEIGHT)
        self.StartButton.clicked.connect(self.__handleStart)
        self.StopButton.clicked.connect(self.__handleStop)
        
        currentSelectionLayout = QHBoxLayout()
        currentSelectionLayout.addWidget(self.__currentPatternLabel)
        currentSelectionLayout.addWidget(self.StartButton)
        currentSelectionLayout.addWidget(self.StopButton)
        currentSelectionLayout.addStretch(1) 
        
        mainLayout.addLayout(currentSelectionLayout)
        mainLayout.addWidget(self.__tabs)
        
        # Make the window knwo what is the main widget
        self.setCentralWidget(mainWidget)


        
    def __Log(self,message):
        self.__log.LOG(self.__logTitle,message)
           
    def __createMenu(self):
        menu = self.menuBar()
        
        fileMenu = menu.addMenu(MainWindow.FILE_MENU)
        
        exitAction = QAction(menu)
        exitAction.setText(MainWindow.EXIT_MENU)
        exitAction.triggered.connect(self.__exit)
        fileMenu.addAction(exitAction)
        
    def __handleStart(self):
        self.__Log("START")
        
    def __handleStop(self):
        self.__Log("STOP")
        
    def __exit(self):
        self.close()
        